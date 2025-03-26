import asyncio
import request
import config

"""
目前仅支持【无需选座】的项目，使用异步请求加速抢票过程
"""
show_id = config.show_id
session_id = config.session_id
buy_count = config.buy_count
audience_idx = config.audience_idx
deliver_method = config.deliver_method
seat_list = config.seat_list
seat_plan_id = ""
session_id_exclude = []  # 被排除掉的场次
price = 0


async def main():
    global \
        session_id, \
        seat_plan_id, \
        price, \
        deliver_method, \
        audience_idx, \
        session_id_exclude

    while True:
        try:
            # 如果没有指定场次，则默认从第一场开始刷
            if not session_id:
                # 如果项目不是在售状态就一直刷，直到变成在售状态拿到场次id，如果有多场，默认拿第一场
                while True:
                    sessions = await request.get_sessions(show_id)
                    if sessions:
                        for i in sessions:
                            if (
                                i["sessionStatus"] == "ON_SALE"
                                or i["sessionStatus"] == "PRE_SALE"
                                and i["bizShowSessionId"] not in session_id_exclude
                            ):
                                session_id = i["bizShowSessionId"]
                                print("session_id:" + session_id)
                                break
                        if session_id:
                            break
                        else:
                            print("未获取到在售状态且符合购票数量需求的session_id")
                            session_id_exclude = []  # 再给自己一次机会，万一被排除掉的场次又放票了呢

            # 并行请求座位信息和余票信息
            seat_plans_task = asyncio.create_task(
                request.get_seat_plans(show_id, session_id)
            )
            seat_count_task = asyncio.create_task(
                request.get_seat_count(show_id, session_id)
            )

            seat_plans = await seat_plans_task
            seat_count = await seat_count_task

            # 收集符合购票数量的座位
            mp = {
                i["seatPlanId"]: (None, None)
                for i in seat_count
                if i["canBuyCount"] >= buy_count
            }

            # 按价格排序
            seat_price_map = []
            for i in seat_plans:
                if i["seatPlanId"] in mp:
                    seat_price_map.append(
                        (i["seatPlanId"], i["seatPlanName"], i["originalPrice"])
                    )

            # 按价格从低到高排序
            seat_price_map.sort(key=lambda x: x[2])

            # 寻找符合条件且最便宜的座位
            for seat_id, seat_name, seat_price in seat_price_map:
                if seat_name in seat_list:
                    seat_plan_id = seat_id
                    price = seat_price
                    break

            # 如果没有拿到seat_plan_id，说明该场次所有座位的余票都不满足购票数量需求，就重新开始刷下一场次
            if not seat_plan_id:
                print(
                    "该场次"
                    + session_id
                    + "没有符合条件的座位，将为你继续搜寻其他在售场次"
                )
                session_id_exclude.append(session_id)  # 排除掉这个场次
                session_id = ""
                continue

            if not deliver_method:
                deliver_method_task = asyncio.create_task(
                    request.get_deliver_method(
                        show_id, session_id, seat_plan_id, price, buy_count
                    )
                )
                deliver_method_result = await deliver_method_task
                deliver_method = deliver_method_result

            print("deliver_method:" + deliver_method)

            if deliver_method == "VENUE_E":
                await request.create_order(
                    show_id,
                    session_id,
                    seat_plan_id,
                    price,
                    buy_count,
                    deliver_method,
                    0,
                    None,
                    None,
                    None,
                    None,
                    None,
                    [],
                )
            else:
                # 预先获取观演人信息和地址信息（如果需要）
                tasks = []
                audiences_task = asyncio.create_task(request.get_audiences())
                tasks.append(audiences_task)

                address_task = None
                if deliver_method == "EXPRESS":
                    address_task = asyncio.create_task(request.get_address())
                    tasks.append(address_task)

                # 等待所有任务完成
                await asyncio.gather(*tasks)

                # 获取观演人信息
                audiences = await audiences_task
                if len(audience_idx) == 0:
                    audience_idx = range(buy_count)
                audience_ids = [audiences[i]["id"] for i in audience_idx]

                if deliver_method == "EXPRESS":
                    # 获取默认收货地址
                    address = await address_task
                    address_id = address["addressId"]  # 地址id
                    location_city_id = address["locationId"]  # 460102
                    receiver = address["username"]  # 收件人
                    cellphone = address["cellphone"]  # 电话
                    detail_address = address["detailAddress"]  # 详细地址

                    # 获取快递费用
                    express_fee = await request.get_express_fee(
                        show_id,
                        session_id,
                        seat_plan_id,
                        price,
                        buy_count,
                        location_city_id,
                    )

                    # 下单
                    await request.create_order(
                        show_id,
                        session_id,
                        seat_plan_id,
                        price,
                        buy_count,
                        deliver_method,
                        express_fee["priceItemVal"],
                        receiver,
                        cellphone,
                        address_id,
                        detail_address,
                        location_city_id,
                        audience_ids,
                    )
                elif (
                    deliver_method == "VENUE"
                    or deliver_method == "E_TICKET"
                    or deliver_method == "ID_CARD"
                ):
                    await request.create_order(
                        show_id,
                        session_id,
                        seat_plan_id,
                        price,
                        buy_count,
                        deliver_method,
                        0,
                        None,
                        None,
                        None,
                        None,
                        None,
                        audience_ids,
                    )
                else:
                    print("不支持的deliver_method:" + deliver_method)
            break
        except Exception as e:
            print(e)
            session_id_exclude.append(session_id)  # 排除掉这个场次
            session_id = ""


if __name__ == "__main__":
    asyncio.run(main())
