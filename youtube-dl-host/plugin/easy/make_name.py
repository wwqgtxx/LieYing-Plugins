# -*- coding: utf-8 -*-
# make_name.py, for lieying_plugin/you-get (parse), plugin/easy/make_name

# 说明: 此文件可用来更改 插件 生成的 最终的 视频标题

# 下面这个 函数 make(), 用于生成 标题
#	函数参数列表及其含义说明
#
#	title		视频标题, 比如 少年四大名捕未删减版第44集
#	title_sub	小标题, 比如 决胜归来大团圆
#	title_no	集数, 电视剧的第几集, 比如 44
#	title_short	视频短标题, 比如 少年四大名捕未删减版
#
#	site		网站名称, 比如 不可说
#
def make(title, title_sub, title_no, title_short, site, num_len):
    
    # 以下生成数字, 集数, 可以更改最小数字长度
    
    # 下面生成 集数 数字, 最小数字长度 默认 是 4, 请修改下面一行
    title_no = num_len(title_no, 4)
    
    # 下面一行, name 就是最终 生成的 标题
    name = '_' + title_no + '_' + title + '_' + title_sub + '_' + site
    
    # 上面的默认情况如下, 生成的 标题 (name) 格式类似
    # _0044_少年四大名捕未删减版第44集_决胜归来大团圆
    # _0002_花千骨第2集_灵虫糖宝初降世
    
    return name

# end make_name.py, last_update 2015-07-13 12:13 GMT+0800 CST


