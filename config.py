# 输入自己的token, 通过devtools查看
token = "eyJ0eXAiOiJKV1QiLCJjdHkiOiJKV1QiLCJ6aXAiOiJERUYiLCJhbGciOiJSUzUxMiJ9.eNqEUcuOgkAQ_Jc-cxhghtcNWY0kGAwrB09khCaS8MowbNY1_vvOoFk9ucfqrqqu7r7CwGd5jvt6gKCf29aAeUJxx1c4NT_RUCEEsNkmxQ4MmObT6q_oWI7LPYJYWabHqOV6Tm1SnyqeUmZDq0mr_LjOVKWTZa6tKy100fIpq23qeX5FCDEJs5ln34X_0RjcFl46ouByeMvVWeRlVEFMFQFFeea9fF33C8XUDD0EtgEjF7KRCwJHCfF7bAQemk7LXWoTaip36voGlAK5fLYsnzHyaE2XSWL3OFEUxsUxLqIkzT-K5RTFPs-ibfi5LvZJeNik2e4-6XWE8lc5e2z1as-39FyP0_j2CwAA__8.eESe83cWQV3bHVFnRmpC9jcDs3RkGhLExWuQmg60CPYGJW5p4QlxZkTDWEjBehKoEM4-F1emKrp9f_sVsKcOmOwNyrlpBX_tPeqxORSjQhX6Wl4Y-BGQxo8qDOL1l1j8xky79IpFrSIE3B-9LB3tYokHuxw0DaIYWKYFvBTeZXY"
# 项目id，必填
show_id = "67bea304935675000197288d"
# 指定场次id，不指定则默认从第一场开始遍历
session_id = ""  # 644fcb7dca916100017dda3d
# 购票数量，一定要看购票须知，不要超过上限
buy_count = 2
# 指定观演人，观演人序号从0开始，人数需与票数保持一致
audience_idx = [0, 1]
# 门票类型，不确定则可以不填，让系统自行判断。快递送票:EXPRESS,电子票:E_TICKET,现场取票:VENUE,电子票或现场取票:VENUE_E,目前只发现这四种，如有新发现可补充
deliver_method = ""
seat_list = [
    "598元",
    "798元",
]  # 票价列表，默认从最低价开始
