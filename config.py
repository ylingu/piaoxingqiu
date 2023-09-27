# 输入自己的token, 通过cyy_gatewayapi/trade/buyer/order查看
token =''
# 项目id，必填
show_id = '6443a0d135bfd50001a7c7db'
# 指定场次id，不指定则默认从第一场开始遍历
session_id = ''  # 644fcb7dca916100017dda3d
# 购票数量，一定要看购票须知，不要超过上限
buy_count = 1
# 指定观演人，观演人序号从0开始，人数需与票数保持一致
audience_idx = [1]
# 门票类型，不确定则可以不填，让系统自行判断。快递送票:EXPRESS,电子票:E_TICKET,现场取票:VENUE,电子票或现场取票:VENUE_E,目前只发现这四种，如有新发现可补充
deliver_method = ''
seat_list = ['四楼427区', '二楼203区']
