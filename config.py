# 输入自己的token, 通过浏览器DevTools查看
access_token = ""
# 项目id，必填
show_id = "67dfc88daebf0d0001a57a06"  # "67bea304935675000197288d"
# 指定场次id，不指定则默认从第一场开始遍历
session_id = ""
# 购票数量，一定要看购票须知，不要超过上限
buy_count = 2
# 指定观演人，观演人序号从0开始，人数需与票数保持一致
audience_idx = [0, 1]
# 门票类型，不确定则可以不填，让系统自行判断。快递送票:EXPRESS,电子票:E_TICKET或ID_CARD,现场取票:VENUE,电子票或现场取票:VENUE_E,目前只发现这五种，如有新发现可补充
deliver_method = ""
seat_list = [
    "两日通票128元",
]  # 票价列表，默认从最低价开始
