# -*- coding: utf-8 -*-
"""
力同 A6 平台 DMR 模组 AT 指令数据库（基于《AM613X_AM614X AT指令串口通信协议V1.8》）
本文件是整个测试工具的"教学核心"：把协议里每条指令的参数含义、取值范围、
适用型号、默认值、示例全部数据化，UI 由它自动生成。
后续新增/修改指令，只改本文件即可。
"""

# 型号列表（用于顶部型号选择器 + 指令过滤）
MODELS = [
    "通用(ALL)", "AM6132", "AM6133", "AM6142", "AU042", "AM6101", "AM6102", "AM6103",
]

# 24bit ID 取值范围说明
ID_RANGE = "1~16776415 (24bit)"

# 指令类别（左侧树的分组）
GROUPS = [
    "连接与测试",
    "频道与频率",
    "功率与发射校准",
    "音频与增益",
    "射频校准",
    "模拟信道功能",
    "呼叫控制",
    "ID与地址",
    "短信与数据",
    "GPIO与ADC",
    "语音播报",
    "省电与维护",
    "天气与其它",
]

# 每条指令结构说明：
#   name    指令名（不含 AT+ 前缀，用于构造发送串）
#   group   所属类别
#   models  适用型号列表，"ALL" 表示全部型号通用
#   desc    指令一句话说明（教学）
#   fmt     发送格式示例（含参数占位）
#   params  参数列表，每项 {name, range, default, note}
#   resp    响应格式与含义
#   example 完整发送示例
COMMANDS = [

    # ===================== 连接与测试 =====================
    {
        "name": "AT+DMOCONNECT", "group": "连接与测试", "models": ["ALL"],
        "desc": "握手命令，证明模块运作正常。终端每发一次，模块回复一次；连续3次无应答应重启模块。",
        "fmt": "AT+DMOCONNECT",
        "params": [],
        "resp": "+DMOCONNECT:X  (X:0-正常接收状态, 1-发射状态)",
        "example": "AT+DMOCONNECT",
    },
    {
        "name": "AT+DMOTESTMODE", "group": "连接与测试", "models": ["ALL"],
        "desc": "进入/退出测试模式。",
        "fmt": "AT+DMOTESTMODE=X",
        "params": [{"name": "X", "range": "1-进入测试模式, 0-退出测试模式", "default": "1", "note": "测试模式开关"}],
        "resp": "+DMOTESTMODE:X  (X:0-成功, 1-数据设置异常)",
        "example": "AT+DMOTESTMODE=1",
    },
    {
        "name": "AT+DMODISCONNECT", "group": "连接与测试", "models": ["ALL"],
        "desc": "测试结束命令。省电功能激活后需执行此命令生效。",
        "fmt": "AT+DMODISCONNECT",
        "params": [],
        "resp": "+DMODISCONNECT:X  (X:0-成功, 1-失败)",
        "example": "AT+DMODISCONNECT",
    },
    {
        "name": "AT+DMOGETSTARTUP", "group": "连接与测试", "models": ["ALL"],
        "desc": "模块上电初始化完成后主动上报状态（非请求，模块自推）。",
        "fmt": "(模块主动上报)",
        "params": [],
        "resp": "+DMOGETSTARTUP:X  (X:0-初始化失败, 1-初始化成功)",
        "example": "(上电后自动上报 +DMOGETSTARTUP:1)",
    },
    {
        "name": "AT+DMOGETSOFTVERSION", "group": "连接与测试", "models": ["ALL"],
        "desc": "获取模块软件版本号。",
        "fmt": "AT+DMOGETSOFTVERSION",
        "params": [],
        "resp": "+DMOGETSOFTVERSION:X  (X:软件版本字符串)",
        "example": "AT+DMOGETSOFTVERSION",
    },
    {
        "name": "AT+DMOGETCHIPID", "group": "连接与测试", "models": ["ALL"],
        "desc": "获取芯片ID。",
        "fmt": "AT+DMOGETCHIPID",
        "params": [],
        "resp": "+DMOGETCHIPID:X  (X:16字节芯片ID，如 0123456789ABCDEF)",
        "example": "AT+DMOGETCHIPID",
    },
    {
        "name": "AT+DMOGETPWRSAVEINFO", "group": "连接与测试", "models": ["ALL"],
        "desc": "获取当前省电功能配置信息。",
        "fmt": "AT+DMOGETPWRSAVEINFO",
        "params": [],
        "resp": "+DMOGETPWRSAVEINFO=X1,X2,X3,X4,X5",
        "example": "AT+DMOGETPWRSAVEINFO",
    },

    # ===================== 频道与频率 =====================
    {
        "name": "AT+DMOSETGROUP", "group": "频道与频率", "models": ["ALL"],
        "desc": "设置模块工作频道参数（最核心的频道配置指令）。",
        "fmt": "AT+DMOSETGROUP=MODE,GBW,TFV,RFV,00,00,SQ,POWER",
        "params": [
            {"name": "MODE", "range": "1-模拟, 2-数字PDT, 3-数字DMR", "default": "3", "note": "工作模式"},
            {"name": "GBW", "range": "0-窄带(12.5K), 1-宽带(25K)", "default": "0", "note": "带宽设置"},
            {"name": "TFV", "range": "100000000~999999999 (Hz)", "default": "409750000", "note": "发射频率值"},
            {"name": "RFV", "range": "100000000~999999999 (Hz)", "default": "409750000", "note": "接收频率值"},
            {"name": "TxResv", "fixed": "00", "note": "保留字段(固定填00，非用户输入)"},
            {"name": "RxResv", "fixed": "00", "note": "保留字段(固定填00，非用户输入)"},
            {"name": "SQ", "range": "0-监听模式, 1~9-静噪等级(1最灵敏,9最严格)", "default": "3", "note": "静噪级别"},
            {"name": "POWER", "range": "0-低功率, 1-高功率, 2-中功率", "default": "1", "note": "发射功率"},
        ],
        "resp": "+DMOSETGROUP:X  (X:0-成功, 1-数据设置异常)",
        "example": "AT+DMOSETGROUP=1,0,409750000,409750000,00,00,3,1",
    },
    {
        "name": "AT+DMOCHSWITCH", "group": "频道与频率", "models": ["ALL"],
        "desc": "信道切换命令（开放全信道 0~15）。",
        "fmt": "AT+DMOCHSWITCH=X",
        "params": [{"name": "X", "range": "0~15", "default": "0", "note": "信道号"}],
        "resp": "+DMOCHSWITCH:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOCHSWITCH=1",
    },
    {
        "name": "AT+DMOSETCHFREQ", "group": "频道与频率", "models": ["ALL"],
        "desc": "设置当前信道发射/接收频率。",
        "fmt": "AT+DMOSETCHFREQ=<txFreq>,<rxFreq>",
        "params": [
            {"name": "txFreq", "range": "100.0000~999.9999 (MHz, 4位小数)", "default": "409.7500", "note": "发射频率"},
            {"name": "rxFreq", "range": "100.0000~999.9999 (MHz, 4位小数)", "default": "409.7500", "note": "接收频率"},
        ],
        "resp": "+DMOSETCHFREQ:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETCHFREQ=409.7500,409.7500",
    },
    {
        "name": "AT+DMOGETCHFREQ", "group": "频道与频率", "models": ["AU042"],
        "desc": "获取指定信道频率信息（AU042）。",
        "fmt": "AT+DMOGETCHFREQ=X",
        "params": [{"name": "X", "range": "0~15", "default": "0", "note": "指定信道号"}],
        "resp": "成功:+DMOGETCHFREQ:DIG,TxFreq,RxFreq,Power,Reserved,colorCode,TimeSlot,Reserved,Reserved,Encry / +DMOGETCHFREQ:ANA,TxFreq,RxFreq,Power,WIDE/NARROW  失败:+DMOGETCHFREQ:0",
        "example": "AT+DMOGETCHFREQ=0",
    },
    {
        "name": "AT+DMOGETCURRCH", "group": "频道与频率", "models": ["ALL"],
        "desc": "获取当前信道信息。",
        "fmt": "AT+DMOGETCURRCH",
        "params": [],
        "resp": "成功:+DMOGETCURRCH:CHx,DIG/ANA,TxFreq,RxFreq,Power,...  失败:+DMOGETCURRCH:0",
        "example": "AT+DMOGETCURRCH",
    },
    {
        "name": "AT+DMOSETFREQBANDNUM", "group": "频道与频率", "models": ["ALL"],
        "desc": "设置频带数（最多20个频带）。",
        "fmt": "AT+DMOSETFREQBANDNUM=X",
        "params": [{"name": "X", "range": "1~20", "default": "20", "note": "频带数"}],
        "resp": "+DMOSETFREQBANDNUM:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETFREQBANDNUM=20",
    },
    {
        "name": "AT+DMOGETFREQBANDNUM", "group": "频道与频率", "models": ["ALL"],
        "desc": "获取频带数。",
        "fmt": "AT+DMOGETFREQBANDNUM",
        "params": [],
        "resp": "+DMOGETFREQBANDNUM:X  (X:频带数 1~20)",
        "example": "AT+DMOGETFREQBANDNUM",
    },
    {
        "name": "AT+DMOSETFREQBANDVAL", "group": "频道与频率", "models": ["ALL"],
        "desc": "设置频带参数值（最多20个频带，逗号分隔）。",
        "fmt": "AT+DMOSETFREQBANDVAL=X1,X2,...X20",
        "params": [{"name": "X1..X20", "range": "0~999999999 (Hz)", "default": "400125000", "note": "各频带参数值，逗号分隔"}],
        "resp": "+DMOSETFREQBANDVAL:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETFREQBANDVAL=400125000,410125000,420125000",
    },
    {
        "name": "AT+DMOGETFREQBANDVAL", "group": "频道与频率", "models": ["ALL"],
        "desc": "获取频带参数值。",
        "fmt": "AT+DMOGETFREQBANDVAL",
        "params": [],
        "resp": "+DMOGETFREQBANDVAL:X1,X2,...X20  (各频带参数值)",
        "example": "AT+DMOGETFREQBANDVAL",
    },
    {
        "name": "AT+SETCOLORCODE", "group": "频道与频率", "models": ["ALL"],
        "desc": "设置当前信道色码（数字模式用）。",
        "fmt": "AT+SETCOLORCODE=X",
        "params": [{"name": "X", "range": "0~15", "default": "1", "note": "色码"}],
        "resp": "+SETCOLORCODE:X  (X:0-成功, 1-失败)",
        "example": "AT+SETCOLORCODE=1",
    },
    {
        "name": "AT+SETTIMESLOT", "group": "频道与频率", "models": ["AM6101", "AM6102", "AM6103"],
        "desc": "设置数字信道时隙（仅 AM6101/6102/6103）。",
        "fmt": "AT+SETTIMESLOT=X",
        "params": [{"name": "X", "range": "1, 2", "default": "1", "note": "时隙号"}],
        "resp": "+SETTIMESLOT:X  (X:0-成功, 1-失败)",
        "example": "AT+SETTIMESLOT=1",
    },
    {
        "name": "AT+SETCHCONTACT", "group": "频道与频率", "models": ["AM6101", "AM6102", "AM6103"],
        "desc": "设置信道联系人ID（仅 AM6101/6102/6103）。",
        "fmt": "AT+SETCHCONTACT=X",
        "params": [{"name": "X", "range": "1~16776415", "default": "1", "note": "联系人ID"}],
        "resp": "+SETCHCONTACT:X  (X:0-成功, 1-失败)",
        "example": "AT+SETCHCONTACT=1",
    },
    {
        "name": "AT+GETINCALLID", "group": "频道与频率", "models": ["AM6101", "AM6102", "AM6103"],
        "desc": "获取数字信道呼入ID（仅 AM6101/6102/6103）。",
        "fmt": "AT+GETINCALLID",
        "params": [],
        "resp": "+GETINCALLID:呼叫类型,呼入ID,呼叫方ID  (呼叫类型:0-个呼,1-组呼,2-全呼)",
        "example": "AT+GETINCALLID",
    },

    # ===================== 功率与发射校准 =====================
    {
        "name": "AT+DMOSETAPC", "group": "功率与发射校准", "models": ["ALL"],
        "desc": "设置模块发射功率（APC粗调档位）。",
        "fmt": "AT+DMOSETAPC=X",
        "params": [{"name": "X", "range": "0~63", "default": "4", "note": "发射功率档位"}],
        "resp": "+DMOSETAPC:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETAPC=4",
    },
    {
        "name": "AT+DMOSETPOWER", "group": "功率与发射校准", "models": ["ALL"],
        "desc": "设置高低功率（呼叫前配置，不发起PTT）。",
        "fmt": "AT+DMOSETPOWER=X",
        "params": [{"name": "X", "range": "0-低功率, 1-高功率, 2-中功率", "default": "1", "note": "功率档"}],
        "resp": "+DMOSETPOWER:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETPOWER=1",
    },
    {
        "name": "AT+SETPOWERAPCGAIN", "group": "功率与发射校准", "models": ["ALL"],
        "desc": "设置APC增益值（A6外部增益，调节发射功率粗调）。",
        "fmt": "AT+SETPOWERAPCGAIN=bandIdx,txPower,ApcGain",
        "params": [
            {"name": "bandIdx", "range": "0~19", "default": "10", "note": "频带序号"},
            {"name": "txPower", "range": "0-低功率, 1-高功率, 2-中功率", "default": "0", "note": "发射功率档"},
            {"name": "ApcGain", "range": "0~255", "default": "200", "note": "APC增益值"},
        ],
        "resp": "+SETPOWERAPCGAIN:X  (X:0-成功, 1-失败)",
        "example": "AT+SETPOWERAPCGAIN=10,0,200",
    },
    {
        "name": "AT+GETPOWERAPCGAIN", "group": "功率与发射校准", "models": ["ALL"],
        "desc": "获取APC增益值（A6外部增益）。",
        "fmt": "AT+GETPOWERAPCGAIN=X",
        "params": [{"name": "X", "range": "0~19", "default": "1", "note": "频带序号"}],
        "resp": "+GETPOWERAPCGAIN:X1~X7  (X1:频带序号, X2:模拟高, X3:模拟中, X4:模拟低, X5:数字高, X6:数字中, X7:数字低)",
        "example": "AT+GETPOWERAPCGAIN=1",
    },
    {
        "name": "AT+SETPOWERAMPGAIN", "group": "功率与发射校准", "models": ["ALL"],
        "desc": "设置AMP增益值（A6内部增益，调节发射功率）。",
        "fmt": "AT+SETPOWERAMPGAIN=X1,X2,X3,X4",
        "params": [
            {"name": "X1", "range": "0~19", "default": "0", "note": "频带序号"},
            {"name": "X2", "range": "1-模拟模式, 2-数字模式", "default": "2", "note": "工作模式"},
            {"name": "X3", "range": "0-低功率, 1-高功率, 2-中功率", "default": "0", "note": "功率档"},
            {"name": "X4", "range": "0~63", "default": "8", "note": "AMP增益值"},
        ],
        "resp": "+SETPOWERAMPGAIN:X  (X:0-成功, 1-失败)",
        "example": "AT+SETPOWERAMPGAIN=0,2,0,8",
    },
    {
        "name": "AT+GETPOWERAMPGAIN", "group": "功率与发射校准", "models": ["ALL"],
        "desc": "获取AMP增益值（A6内部增益）。",
        "fmt": "AT+GETPOWERAMPGAIN=X",
        "params": [{"name": "X", "range": "0~19", "default": "1", "note": "频带序号"}],
        "resp": "+GETPOWERAMPGAIN:X1~X7  (X1:频带序号, X2~X7:模拟/数字 高/中/低功率AMP增益)",
        "example": "AT+GETPOWERAMPGAIN=1",
    },
    {
        "name": "AT+SETAPC_FINEVALUE", "group": "功率与发射校准", "models": ["ALL"],
        "desc": "设置APC微调值（A6v2芯片，粗调补充，微调发射功率）。",
        "fmt": "AT+SETAPC_FINEVALUE=bandIdx,txPower,ApcFine",
        "params": [
            {"name": "bandIdx", "range": "0~20", "default": "10", "note": "频带序号"},
            {"name": "txPower", "range": "0-低功率, 1-高功率, 2-中功率", "default": "0", "note": "功率档"},
            {"name": "ApcFine", "range": "0~3", "default": "3", "note": "APC微调值"},
        ],
        "resp": "+SETAPC_FINEVALUE:X  (X:0-成功, 1-失败)",
        "example": "AT+SETAPC_FINEVALUE=10,0,3",
    },
    {
        "name": "AT+GETAPC_FINEVALUE", "group": "功率与发射校准", "models": ["ALL"],
        "desc": "获取APC微调值（A6v2芯片）。",
        "fmt": "AT+GETAPC_FINEVALUE=X",
        "params": [{"name": "X", "range": "0~20", "default": "10", "note": "频带序号"}],
        "resp": "+GETAPC_FINEVALUE:X1~X7  (X1:频带序号, X2~X7:模拟/数字 高/中/低功率APC微调值)",
        "example": "AT+GETAPC_FINEVALUE=10",
    },
    {
        "name": "AT+DMOAMPCTRLTEST", "group": "功率与发射校准", "models": ["ALL"],
        "desc": "调节发射功率增益值（测试命令，调A6内部增益）。",
        "fmt": "AT+DMOAMPCTRLTEST=X",
        "params": [{"name": "X", "range": "0~63", "default": "2", "note": "增益值"}],
        "resp": "+DMOAMPCTRLTEST:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOAMPCTRLTEST=2",
    },
    {
        "name": "AT+DMOAPCCTRLTEST", "group": "功率与发射校准", "models": ["ALL"],
        "desc": "调节栅压增益值（测试命令，调外部PA增益）。",
        "fmt": "AT+DMOAPCCTRLTEST=X",
        "params": [{"name": "X", "range": "0~255", "default": "108", "note": "栅压增益值"}],
        "resp": "+DMOAPCCTRLTEST:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOAPCCTRLTEST=108",
    },
    {
        "name": "AT+SETPOWERAPCSW", "group": "功率与发射校准", "models": ["ALL"],
        "desc": "设置APC输出电流使能（非模块使用指令，调发射电流）。",
        "fmt": "AT+SETPOWERAPCSW=X1",
        "params": [{"name": "X1", "range": "1-打开(使能PA), 0-关闭", "default": "1", "note": "APC电压输出使能"}],
        "resp": "+SETPOWERAPCSW:X  (X:0-成功, 1-失败)",
        "example": "AT+SETPOWERAPCSW=1",
    },
    {
        "name": "AT+DMR_ADJTXSYMDEV", "group": "功率与发射校准", "models": ["ALL"],
        "desc": "调节DMR发射符号频偏值。",
        "fmt": "AT+DMR_ADJTXSYMDEV=X",
        "params": [{"name": "X", "range": "0~20000", "default": "9420", "note": "DMR发射符号频偏值"}],
        "resp": "+DMR_ADJTXSYMDEV:X  (X:0-成功, 1-失败)",
        "example": "AT+DMR_ADJTXSYMDEV=9420",
    },
    {
        "name": "AT+DMR_GETTXSYMDEV", "group": "功率与发射校准", "models": ["ALL"],
        "desc": "获取DMR发射符号频偏值。",
        "fmt": "AT+DMR_GETTXSYMDEV",
        "params": [],
        "resp": "+DMR_GETTXSYMDEV:X  (X:频偏值)",
        "example": "AT+DMR_GETTXSYMDEV",
    },
    {
        "name": "AT+SETPROFILERAMPSSHIFT", "group": "功率与发射校准", "models": ["ALL"],
        "desc": "设置3920B的profile ramps平移值。",
        "fmt": "AT+SETPROFILERAMPSSHIFT=X1",
        "params": [{"name": "X1", "range": "0~255", "default": "18", "note": "平移值"}],
        "resp": "+SETPROFILERAMPSSHIFT:X  (X:0-成功, 1-失败)",
        "example": "AT+SETPROFILERAMPSSHIFT=18",
    },
    {
        "name": "AT+SETPROFILERAMPSDWPOS", "group": "功率与发射校准", "models": ["ALL"],
        "desc": "设置3920B的profile ramps下坡位置值。",
        "fmt": "AT+SETPROFILERAMPSDWPOS=X1",
        "params": [{"name": "X1", "range": "0~20000", "default": "10000", "note": "下坡位置值"}],
        "resp": "+SETPROFILERAMPSDWPOS:X  (X:0-成功, 1-失败)",
        "example": "AT+SETPROFILERAMPSDWPOS=10000",
    },
    {
        "name": "AT+GETPROFILERAMPS", "group": "功率与发射校准", "models": ["ALL"],
        "desc": "获取3920B的profile ramps参数。",
        "fmt": "AT+GETPROFILERAMPS",
        "params": [],
        "resp": "+GETPROFILERAMPS:X1,X2,X3,X4  (X1:平移值, X2:下坡位置值, X3/X4:保留)",
        "example": "AT+GETPROFILERAMPS",
    },

    # ===================== 音频与增益 =====================
    {
        "name": "AT+DMOSETMIC", "group": "音频与增益", "models": ["ALL"],
        "desc": "设置模块麦克风数字增益。",
        "fmt": "AT+DMOSETMIC=X",
        "params": [{"name": "X", "range": "0~15", "default": "4", "note": "麦克风数字增益"}],
        "resp": "+DMOSETMIC:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETMIC=4",
    },
    {
        "name": "AT+DMOSETVOLUME", "group": "音频与增益", "models": ["ALL"],
        "desc": "设置模块扬声器(SPK)数字增益。",
        "fmt": "AT+DMOSETVOLUME=X",
        "params": [{"name": "X", "range": "0~31", "default": "18", "note": "SPK数字增益"}],
        "resp": "+DMOSETVOLUME:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETVOLUME=18",
    },
    {
        "name": "AT+DMOSETVOLUMELEVEL", "group": "音频与增益", "models": ["ALL"],
        "desc": "设置音量等级（非模块使用指令）。",
        "fmt": "AT+DMOSETVOLUMELEVEL=X1",
        "params": [{"name": "X1", "range": "0-静音, 1~10-音量等级", "default": "1", "note": "音量等级"}],
        "resp": "+DMOSETVOLUMELEVEL:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETVOLUMELEVEL=1",
    },
    {
        "name": "AT+DMOSETVOX", "group": "音频与增益", "models": ["ALL"],
        "desc": "设置模块VOX(声控)功能开关和级别。",
        "fmt": "AT+DMOSETVOX=X",
        "params": [{"name": "X", "range": "0-关闭, 1~8-声控等级(越小越灵敏)", "default": "4", "note": "声控等级"}],
        "resp": "+DMOSETVOX:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETVOX=4",
    },
    {
        "name": "AT+SETVOX", "group": "音频与增益", "models": ["ALL"],
        "desc": "设置声控等级（数字模式常用）。",
        "fmt": "AT+SETVOX=X",
        "params": [{"name": "X", "range": "0-关闭, 1~3-声控等级(启动声控)", "default": "1", "note": "声控等级"}],
        "resp": "+SETVOX:X  (X:0-成功, 1-失败)",
        "example": "AT+SETVOX=1",
    },
    {
        "name": "AT+SETEQUALIZER", "group": "音频与增益", "models": ["AM6132"],
        "desc": "设置数字/模拟均衡器（仅 AM6132/dev）。",
        "fmt": "AT+SETEQUALIZER=x1,x2,x3,x4",
        "params": [
            {"name": "x1", "range": "0-关闭, 1-开启(需为1才生效)", "default": "1", "note": "均衡器开关"},
            {"name": "x2", "range": "-12~12 (400Hz波段)", "default": "-3", "note": "400Hz增益"},
            {"name": "x3", "range": "-12~12 (1000Hz波段)", "default": "12", "note": "1000Hz增益"},
            {"name": "x4", "range": "-12~12 (2500Hz波段)", "default": "0", "note": "2500Hz增益"},
        ],
        "resp": "+SETEQUALIZER:X  (X:0-成功, 1-失败)",
        "example": "AT+SETEQUALIZER=1,-3,12,0",
    },
    {
        "name": "AT+DMOPLAYTONE", "group": "音频与增益", "models": ["ALL"],
        "desc": "播放提示音。",
        "fmt": "AT+DMOPLAYTONE=X",
        "params": [{"name": "X", "range": "0~20", "default": "1", "note": "提示音编号"}],
        "resp": "+DMOPLAYTONE:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOPLAYTONE=1",
    },
    {
        "name": "AT+SETTONELIST", "group": "音频与增益", "models": ["ALL"],
        "desc": "设置提示音列表（最多8个列表，每个最多14个音频[时长ms,频率Hz]）。",
        "fmt": "AT+SETTONELIST=x1,x2,x3,...x29",
        "params": [
            {"name": "x1", "range": "1~8 (列表编号)", "default": "1", "note": "提示音列表编号"},
            {"name": "x2..x29", "range": "时长ms,频率Hz 成对(最多14对)", "default": "50,400,75,600", "note": "音频组合(时长,频率)成对"},
        ],
        "resp": "+SETTONELIST:X  (X:0-成功, 1-失败)",
        "example": "AT+SETTONELIST=1,50,400,75,600",
    },
    {
        "name": "AT+SETALERTTONE", "group": "音频与增益", "models": ["ALL"],
        "desc": "设置提示音（将某类提示音绑定到已设置的提示音列表）。",
        "fmt": "AT+SETALERTTONE=x1,x2",
        "params": [
            {"name": "x1", "range": "1-呼出,2-语音结束,3-呼叫结束,4-短信接收,5-低电报警", "default": "1", "note": "提示音类型"},
            {"name": "x2", "range": "1~8 (SETTONELIST设置的列表编号)", "default": "2", "note": "提示音列表编号"},
        ],
        "resp": "+SETALERTTONE:X  (X:0-成功, 1-失败)",
        "example": "AT+SETALERTTONE=1,2",
    },
    {
        "name": "AT+SETBEEP", "group": "音频与增益", "models": ["AM6101", "AM6102", "AM6103"],
        "desc": "设置提示音开关（仅 AM6101/6102/6103）。",
        "fmt": "AT+SETBEEP=X1",
        "params": [{"name": "X1", "range": "0-关闭, 1-开启", "default": "1", "note": "提示音开关"}],
        "resp": "+SETBEEP:X  (X:0-成功, 1-失败)",
        "example": "AT+SETBEEP=1",
    },
    {
        "name": "AT+GETSQSTATS", "group": "音频与增益", "models": ["AM6101", "AM6102", "AM6103"],
        "desc": "主动获取SQ(静噪)状态（仅 AM6101/6102/6103）。",
        "fmt": "AT+GETSQSTATS",
        "params": [],
        "resp": "+GETSQSTATS:X  (X:0-无SQ信号, 1-有SQ信号)",
        "example": "AT+GETSQSTATS",
    },
    {
        "name": "AT+GETSQLEVEL", "group": "音频与增益", "models": ["ALL"],
        "desc": "获取SQ(静噪)等级。",
        "fmt": "AT+GETSQLEVEL",
        "params": [],
        "resp": "+GETSQLEVEL:X  (X:SQ等级值)",
        "example": "AT+GETSQLEVEL",
    },
    {
        "name": "AT+DMOGETSQSTATUS", "group": "音频与增益", "models": ["ALL"],
        "desc": "模块检测到有效载波时主动上报SQ状态（需打开speaker）。",
        "fmt": "(模块主动上报)",
        "params": [],
        "resp": "+DMOGETSQSTATUS:X  (X:0-close, 1-open)",
        "example": "(检测到载波时自动上报 +DMOGETSQSTATUS:1)",
    },

    # ===================== 射频校准 =====================
    {
        "name": "AT+DMOSETVAFC", "group": "射频校准", "models": ["ALL"],
        "desc": "调整自动频率控制(AFC)参数。",
        "fmt": "AT+DMOSETVAFC=X",
        "params": [{"name": "X", "range": "0~4095", "default": "1380", "note": "AFC参数"}],
        "resp": "+DMOSETVAFC:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETVAFC=1380",
    },
    {
        "name": "AT+DMOGETVAFC", "group": "射频校准", "models": ["ALL"],
        "desc": "获取自动频率控制(AFC)参数。",
        "fmt": "AT+DMOGETVAFC",
        "params": [],
        "resp": "+DMOGETVAFC:X  (X:0~4095)",
        "example": "AT+DMOGETVAFC",
    },
    {
        "name": "AT+DMOSETRSSIPARAM", "group": "射频校准", "models": ["ALL"],
        "desc": "调整RSSI校准参数。",
        "fmt": "AT+DMOSETRSSIPARAM=X",
        "params": [{"name": "X", "range": "91~101", "default": "96", "note": "RSSI校准参数"}],
        "resp": "+DMOSETRSSIPARAM:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETRSSIPARAM=96",
    },
    {
        "name": "AT+DMOGETRSSIPARAM", "group": "射频校准", "models": ["ALL"],
        "desc": "获取RSSI校准参数。",
        "fmt": "AT+DMOGETRSSIPARAM",
        "params": [],
        "resp": "+DMOGETRSSIPARAM:X  (X:91~101)",
        "example": "AT+DMOGETRSSIPARAM",
    },
    {
        "name": "AT+DMOSETLNAOFFS", "group": "射频校准", "models": ["ALL"],
        "desc": "调整LNA参数（模块计算RSSI会加上LNA增益偏移量）。",
        "fmt": "AT+DMOSETLNAOFFS=X",
        "params": [{"name": "X", "range": "dBm", "default": "0", "note": "LNA偏移量(dBm)"}],
        "resp": "+DMOSETLNAOFFS:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETLNAOFFS=0",
    },
    {
        "name": "AT+DMOGETLNAOFFS", "group": "射频校准", "models": ["ALL"],
        "desc": "获取LNA参数。",
        "fmt": "AT+DMOGETLNAOFFS",
        "params": [],
        "resp": "+DMOGETLNAOFFS:X  (X:dBm)",
        "example": "AT+DMOGETLNAOFFS",
    },
    {
        "name": "AT+DMORDRSSI", "group": "射频校准", "models": ["ALL"],
        "desc": "读取RSSI值（单位dBm，与8920主信号强度对应）。",
        "fmt": "AT+DMORDRSSI",
        "params": [],
        "resp": "+DMORDRSSI:X  (X:RSSI值 dBm)",
        "example": "AT+DMORDRSSI",
    },
    {
        "name": "AT+DMOGETRXBER", "group": "射频校准", "models": ["ALL"],
        "desc": "获取接收误码率(Rx BER)。",
        "fmt": "AT+DMOGETRXBER",
        "params": [],
        "resp": "+DMOGETRXBER:X1,X2,X3  (X1:瞬时值, X2:平均值, X3:0-有效/1-无效)",
        "example": "AT+DMOGETRXBER",
    },
    {
        "name": "AT+DMOSETSMARTLO", "group": "射频校准", "models": ["ALL"],
        "desc": "智能本振设置（0-关闭，1-打开）。",
        "fmt": "AT+DMOSETSMARTLO=X",
        "params": [{"name": "X", "range": "0-关闭, 1-打开", "default": "0", "note": "智能本振开关"}],
        "resp": "+DMOSETSMARTLO:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETSMARTLO=0",
    },
    {
        "name": "AT+SETEFLTRXADJ", "group": "射频校准", "models": ["ALL"],
        "desc": "设置接收电调谐参数（调接收灵敏度，需硬件支持）。",
        "fmt": "AT+SETEFLTRXADJ=X1,X2,X3",
        "params": [
            {"name": "X1", "range": "0~20", "default": "0", "note": "频带序号"},
            {"name": "X2", "range": "0~4095", "default": "2600", "note": "DAC值"},
            {"name": "X3", "range": "0~15", "default": "6", "note": "DAC增益"},
        ],
        "resp": "+SETEFLTRXADJ:X  (X:0-成功, 1-失败)",
        "example": "AT+SETEFLTRXADJ=0,2600,6",
    },
    {
        "name": "AT+GETEFLTRXADJ", "group": "射频校准", "models": ["ALL"],
        "desc": "读取接收电调谐参数。",
        "fmt": "AT+GETEFLTRXADJ=X",
        "params": [{"name": "X", "range": "0~20", "default": "0", "note": "频带序号"}],
        "resp": "+GETEFLTRXADJ:X1,X2,X3  (X1:频带序号, X2:DAC值, X3:DAC增益)",
        "example": "AT+GETEFLTRXADJ=0",
    },
    {
        "name": "AT+SETIMAGEREJEMODE", "group": "射频校准", "models": ["ALL"],
        "desc": "进入/退出镜像抑制调试模式（仅模拟信道下）。",
        "fmt": "AT+SETIMAGEREJEMODE=X1",
        "params": [{"name": "X1", "range": "1-进入调试模式, 0-退出并储存参数", "default": "1", "note": "调试模式开关"}],
        "resp": "+SETIMAGEREJEMODE:X  (X:0-成功, 1-失败)",
        "example": "AT+SETIMAGEREJEMODE=1",
    },
    {
        "name": "AT+SETIMAGEREJE", "group": "射频校准", "models": ["ALL"],
        "desc": "设置镜像抑制（仅模拟信道，需先进入调试模式）。",
        "fmt": "AT+SETIMAGEREJE=X1,X2,X3",
        "params": [
            {"name": "X1", "range": "0~20 (校准频段, band0:136~140MHz...band9:400~410MHz...band20:510~520MHz)", "default": "0", "note": "校准频段"},
            {"name": "X2", "range": "0~4095", "default": "1900", "note": "幅度补偿"},
            {"name": "X3", "range": "0~255", "default": "195", "note": "相位补偿"},
        ],
        "resp": "+SETIMAGEREJE:X  (X:0-成功, 1-失败)",
        "example": "AT+SETIMAGEREJE=0,1900,195",
    },
    {
        "name": "AT+GETIMAGEREJE", "group": "射频校准", "models": ["ALL"],
        "desc": "获取当前频带镜像抑制校准值。",
        "fmt": "AT+GETIMAGEREJE=X1",
        "params": [{"name": "X1", "range": "0~20", "default": "1", "note": "读取频段"}],
        "resp": "+GETIMAGEREJE:X1,X2,X3  (X1:频段, X2:幅度补偿, X3:相位补偿)",
        "example": "AT+GETIMAGEREJE=1",
    },
    {
        "name": "AT+DMOSETTAILFREQ", "group": "射频校准", "models": ["ALL"],
        "desc": "设置模拟信道消尾音频率。",
        "fmt": "AT+DMOSETTAILFREQ=freq",
        "params": [{"name": "freq", "range": "0-关闭, 550~2550-开(消尾音频率=freq/10)", "default": "620", "note": "消尾音频率参数"}],
        "resp": "+DMOSETTAILFREQ:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETTAILFREQ=620",
    },

    # ===================== 模拟信道功能 =====================
    {
        "name": "AT+DMOSETCTCDCS", "group": "模拟信道功能", "models": ["ALL"],
        "desc": "设置模拟信道亚音码（CTCSS/CDCSS）。",
        "fmt": "AT+DMOSETCTCDCS=mode,ctdcsType,ctdcsNum,invert",
        "params": [
            {"name": "mode", "range": "0-发射亚音, 1-接收亚音", "default": "0", "note": "发射/接收选择"},
            {"name": "ctdcsType", "range": "0-无亚音, 1-CTCSS, 2-CDCSS", "default": "1", "note": "亚音类型"},
            {"name": "ctdcsNum", "range": "CTCSS:1~50标准,550~2550非标准(=freq*10); CDCSS:0~777", "default": "670", "note": "亚音码"},
            {"name": "invert", "range": "CTCSS无效; CDCSS:0-正码,1-反码", "default": "0", "note": "反码(仅CDCSS)"},
        ],
        "resp": "+DMOSETCTCDCS:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETCTCDCS=0,1,670,0",
    },
    {
        "name": "AT+DMOSETCTCDCSGAIN", "group": "模拟信道功能", "models": ["ALL"],
        "desc": "设置亚音调制频偏。",
        "fmt": "AT+DMOSETCTCDCSGAIN=ctcdcsType,gain",
        "params": [
            {"name": "ctcdcsType", "range": "1-CTCSS, 2-CDCSS", "default": "1", "note": "亚音类型"},
            {"name": "gain", "range": "0~32767", "default": "20000", "note": "亚音幅度增益"},
        ],
        "resp": "+DMOSETCTCDCSGAIN:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETCTCDCSGAIN=1,20000",
    },
    {
        "name": "AT+SETSCRAMBLER", "group": "模拟信道功能", "models": ["ALL"],
        "desc": "设置当前信道扰频功能开关（仅模拟信道有效）。",
        "fmt": "AT+SETSCRAMBLER=X",
        "params": [{"name": "X", "range": "0-OFF, 1-ON", "default": "1", "note": "扰频开关"}],
        "resp": "+SETSCRAMBLER:X  (X:0-成功, 1-失败)",
        "example": "AT+SETSCRAMBLER=1",
    },
    {
        "name": "AT+SETCOMPANDER", "group": "模拟信道功能", "models": ["ALL"],
        "desc": "设置压扩功能开关（仅模拟信道有效）。",
        "fmt": "AT+SETCOMPANDER=X",
        "params": [{"name": "X", "range": "0-OFF, 1-ON", "default": "1", "note": "压扩开关"}],
        "resp": "+SETCOMPANDER:X  (X:0-成功, 1-失败)",
        "example": "AT+SETCOMPANDER=1",
    },
    {
        "name": "AT+DMOSETPWRSAVELV", "group": "模拟信道功能", "models": ["ALL"],
        "desc": "设置模拟省电等级（仅模拟模式生效，缺省关闭）。",
        "fmt": "AT+DMOSETPWRSAVELV=X",
        "params": [{"name": "X", "range": "0~9 (0-关闭省电)", "default": "4", "note": "省电等级(如4表示1:4)"}],
        "resp": "+DMOSETPWRSAVELV:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETPWRSAVELV=4",
    },
    {
        "name": "AT+DMODIGPWRSAVECTRL", "group": "模拟信道功能", "models": ["ALL"],
        "desc": "数字省电控制（仅数字模式生效，缺省关闭）。",
        "fmt": "AT+DMODIGPWRSAVECTRL=X1,X2",
        "params": [
            {"name": "X1", "range": "1-打开数字省电, 0-关闭", "default": "1", "note": "数字省电开关"},
            {"name": "X2", "range": "100~1000 (ms)", "default": "240", "note": "睡眠时间"},
        ],
        "resp": "+DMODIGPWRSAVECTRL:X  (X:0-成功, 1-失败)",
        "example": "AT+DMODIGPWRSAVECTRL=1,240",
    },

    # ===================== 呼叫控制 =====================
    {
        "name": "AT+DMOPTT", "group": "呼叫控制", "models": ["ALL"],
        "desc": "PTT发射控制（1-按下发射，0-松开）。呼叫类指令需在其前配置。",
        "fmt": "AT+DMOPTT=X",
        "params": [{"name": "X", "range": "1-PTT ON, 0-PTT OFF", "default": "1", "note": "PTT控制"}],
        "resp": "+DMOPTT:X  (ON:0-成功,1-已发射,2-中转激活失败; OFF:0-成功,1-失败)",
        "example": "AT+DMOPTT=1",
    },
    {
        "name": "AT+DMOGRPCALLREQ", "group": "呼叫控制", "models": ["ALL"],
        "desc": "组呼请求（仅配置参数，不发起PTT，须在AT+DMOPTT前发）。",
        "fmt": "AT+DMOGRPCALLREQ=X",
        "params": [{"name": "X", "range": ID_RANGE, "default": "3", "note": "请求呼叫的组ID"}],
        "resp": "+DMOGRPCALLREQ:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOGRPCALLREQ=3",
    },
    {
        "name": "AT+DMOINDCALLREQ", "group": "呼叫控制", "models": ["ALL"],
        "desc": "个呼请求（仅配置参数，须在AT+DMOPTT前发）。",
        "fmt": "AT+DMOINDCALLREQ=X",
        "params": [{"name": "X", "range": ID_RANGE, "default": "201", "note": "请求呼叫的个呼ID"}],
        "resp": "+DMOINDCALLREQ:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOINDCALLREQ=201",
    },
    {
        "name": "AT+DMOALLCALLREQ", "group": "呼叫控制", "models": ["ALL"],
        "desc": "全呼请求（仅配置参数，须在AT+DMOPTT前发）。",
        "fmt": "AT+DMOALLCALLREQ",
        "params": [],
        "resp": "+DMOALLCALLREQ:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOALLCALLREQ",
    },
    {
        "name": "AT+SETEMERGENCYCALL", "group": "呼叫控制", "models": ["AM6132"],
        "desc": "紧急呼叫设置（仅配置参数，发呼需再AT+DMOPTT=1，仅 AM6132/dev）。",
        "fmt": "AT+SETEMERGENCYCALL=x1",
        "params": [{"name": "x1", "range": "紧急呼叫目标地址(报警组呼地址)", "default": "1", "note": "目标地址"}],
        "resp": "+SETEMERGENCYCALL:X  (X:0-成功, 1-失败)",
        "example": "AT+SETEMERGENCYCALL=1",
    },
    {
        "name": "AT+SETGROUPVOICEDISABLE", "group": "呼叫控制", "models": ["ALL"],
        "desc": "设置禁止组呼语音接收。",
        "fmt": "AT+SETGROUPVOICEDISABLE=X",
        "params": [{"name": "X", "range": "0-不禁止, 1-禁止组呼语音接收", "default": "1", "note": "禁止开关"}],
        "resp": "+SETGROUPVOICEDISABLE:X  (X:0-成功, 1-失败)",
        "example": "AT+SETGROUPVOICEDISABLE=1",
    },
    {
        "name": "AT+SETRXGROUPLIST", "group": "呼叫控制", "models": ["ALL"],
        "desc": "接收组呼ID设置（0表示清除所有接收组呼）。",
        "fmt": "AT+SETRXGROUPLIST=X1,X2,...Xn",
        "params": [
            {"name": "X1", "range": "0~32 (接收组呼个数, 0=清除)", "default": "3", "note": "组呼个数"},
            {"name": "X2..Xn", "range": "1~16776415", "default": "111,222,333", "note": "接收组呼ID列表"},
        ],
        "resp": "+SETRXGROUPLIST:X  (X:0-成功, 1-失败)",
        "example": "AT+SETRXGROUPLIST=3,111,222,333",
    },
    {
        "name": "AT+SENDSERVER", "group": "呼叫控制", "models": ["AM6132"],
        "desc": "发送补充业务（遥毙/激活/呼叫提示等，仅 AM6132/dev）。",
        "fmt": "AT+SENDSERVER=x1,x2",
        "params": [
            {"name": "x1", "range": "1-遥毙,2-激活,3-呼叫提示,4-对讲机检查,5-远程监听,6-紧急警报", "default": "3", "note": "业务类型"},
            {"name": "x2", "range": "1~16776415 (目标地址; 紧急警报填报警组呼地址)", "default": "201", "note": "目标地址"},
        ],
        "resp": "+SENDSERVER:X  (X:0-成功, 1-失败)",
        "example": "AT+SENDSERVER=1,201",
    },
    {
        "name": "AT+GETSERVERTYPE", "group": "呼叫控制", "models": ["AM6132"],
        "desc": "接收补充业务类型（模块主动上报，仅 AM6132）。",
        "fmt": "(模块主动上报)",
        "params": [],
        "resp": "+GETSERVERTYPE:X1,X2  (X1:1-遥毙,2-激活,3-呼叫提示,4-检查,5-监听,6-警报; X2:发送方ID)",
        "example": "(收到补充业务时自动上报 +GETSERVERTYPE:3,202112)",
    },

    # ===================== ID与地址 =====================
    {
        "name": "AT+DMOSETWLKTLKID", "group": "ID与地址", "models": ["ALL"],
        "desc": "设置对讲模块ID（仅数字模式有效）。",
        "fmt": "AT+DMOSETWLKTLKID=X",
        "params": [{"name": "X", "range": ID_RANGE, "default": "301", "note": "wakie-talkie id"}],
        "resp": "+DMOSETWLKTLKID:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETWLKTLKID=301",
    },
    {
        "name": "AT+DMOGETWLKTLKID", "group": "ID与地址", "models": ["ALL"],
        "desc": "获取对讲模块ID。",
        "fmt": "AT+DMOGETWLKTLKID",
        "params": [],
        "resp": "+DMOGETWLKTLKID:X  (X:wakie-talkie id)",
        "example": "AT+DMOGETWLKTLKID",
    },
    {
        "name": "AT+DMOSETGRPADDR", "group": "ID与地址", "models": ["ALL"],
        "desc": "设置对讲模块组ID（仅数字模式有效）。",
        "fmt": "AT+DMOSETGRPADDR=X",
        "params": [{"name": "X", "range": ID_RANGE, "default": "3", "note": "group addr"}],
        "resp": "+DMOSETGRPADDR:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETGRPADDR=3",
    },
    {
        "name": "AT+DMOGETGRPADDR", "group": "ID与地址", "models": ["ALL"],
        "desc": "获取对讲模块组ID。",
        "fmt": "AT+DMOGETGRPADDR",
        "params": [],
        "resp": "+DMOGETGRPADDR:X  (X:group id)",
        "example": "AT+DMOGETGRPADDR",
    },
    {
        "name": "AT+DMOSETLCHEADERCNT", "group": "ID与地址", "models": ["ALL"],
        "desc": "设置LC头加密。",
        "fmt": "AT+DMOSETLCHEADERCNT=x",
        "params": [{"name": "x", "range": "3~8", "default": "8", "note": "加密数据"}],
        "resp": "+DMOSETLCHEADERCNT:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSETLCHEADERCNT=8",
    },

    # ===================== 短信与数据 =====================
    {
        "name": "AT+SENDMSG", "group": "短信与数据", "models": ["AM6101", "AM6102", "AM6103"],
        "desc": "发送短信息（仅 AM6101/6102/6103）。",
        "fmt": "AT+SENDMSG=X1,X2,X3,XXXXXXXXX",
        "params": [
            {"name": "X1", "range": "0-个呼, 1-组呼", "default": "0", "note": "呼叫类型"},
            {"name": "X2", "range": "1~16776415", "default": "1", "note": "目标ID"},
            {"name": "X3", "range": "短信字节数(不含结束符, <=128)", "default": "7", "note": "短信长度"},
            {"name": "XXXXXXXXX", "range": "短信息内容", "default": "123456#", "note": "短信内容"},
        ],
        "resp": "+SENDMSG:X  (X:0-成功, 1-失败)",
        "example": "AT+SENDMSG=0,1,7,123456#",
    },
    {
        "name": "AT+DMOGETSHORTMSG", "group": "短信与数据", "models": ["AM6101", "AM6102", "AM6103"],
        "desc": "接收短信息（模块主动上报）。",
        "fmt": "(模块主动上报)",
        "params": [],
        "resp": "+DMOGETSHORTMSG:X1,X2,X3:XXXXXX  (X1:源地址, X2:目标地址, X3:0-个呼短信/1-组呼短信)",
        "example": "(收到短信自动上报 +DMOGETSHORTMSG:2021,201,0:abcdefg)",
    },
    {
        "name": "AT+SETSHORTMSGFORMAT", "group": "短信与数据", "models": ["ALL"],
        "desc": "设置短信传输格式（互通性用）。",
        "fmt": "AT+SETSHORTMSGFORMAT:X",
        "params": [{"name": "X", "range": "0-IP压缩(与海能达/摩托互通), 1-定义数据(仅海能达), 2-IP数据(仅摩托)", "default": "0", "note": "短信格式"}],
        "resp": "+SETSHORTMSGFORMAT:X  (X:0-成功, 1-失败)",
        "example": "AT+SETSHORTMSGFORMAT=0",
    },
    {
        "name": "AT+BINARY", "group": "短信与数据", "models": ["AU042"],
        "desc": "用户数据下发命令（AU042）。",
        "fmt": "AT+BINARY=X",
        "params": [{"name": "X", "range": "用户二进制数据", "default": "00110100101011011110000111000", "note": "二进制数据"}],
        "resp": "+BINARY:X,<param>  (X:用户返回值)",
        "example": "AT+BINARY=00110100101011011110000111000",
    },

    # ===================== GPIO与ADC =====================
    {
        "name": "AT+SETGPIODIR", "group": "GPIO与ADC", "models": ["ALL"],
        "desc": "设置GPIO方向（开放GPIO2,4,5,8,17,19,20,21,26,27）。",
        "fmt": "AT+SETGPIODIR=X1,X2",
        "params": [
            {"name": "X1", "range": "0~31 (GPIO管脚号, 仅上述开放脚有效)", "default": "2", "note": "GPIO管脚号"},
            {"name": "X2", "range": "0-输出, 1-输入", "default": "1", "note": "方向"},
        ],
        "resp": "+SETGPIODIR:X  (X:0-成功, 1-失败)",
        "example": "AT+SETGPIODIR=2,1",
    },
    {
        "name": "AT+SETGPIOVALUE", "group": "GPIO与ADC", "models": ["ALL"],
        "desc": "设置GPIO输出高低电平。",
        "fmt": "AT+SETGPIOVALUE=X1,X2",
        "params": [
            {"name": "X1", "range": "0~31 (GPIO管脚号)", "default": "2", "note": "GPIO管脚号"},
            {"name": "X2", "range": "0-输出低电平, 1-输出高电平", "default": "1", "note": "输出电平"},
        ],
        "resp": "+SETGPIOVALUE:X  (X:0-成功, 1-失败)",
        "example": "AT+SETGPIOVALUE=2,1",
    },
    {
        "name": "AT+GETGPIOVALUE", "group": "GPIO与ADC", "models": ["ALL"],
        "desc": "获取GPIO输入值（高低电平）。",
        "fmt": "AT+GETGPIOVALUE=X",
        "params": [{"name": "X", "range": "0~31 (GPIO管脚号)", "default": "2", "note": "GPIO管脚号"}],
        "resp": "+GETGPIOVALUE:X  (X:0-低电平, 1-高电平)",
        "example": "AT+GETGPIOVALUE=2",
    },
    {
        "name": "AT+SETGPADCCHAN", "group": "GPIO与ADC", "models": ["ALL"],
        "desc": "设置(打开/关闭)ADC通道。",
        "fmt": "AT+SETGPADCCHAN=X1,X2",
        "params": [
            {"name": "X1", "range": "0-GPADC channel 0, 1-GPADC channel 1", "default": "0", "note": "ADC通道号"},
            {"name": "X2", "range": "1-打开, 0-关闭", "default": "1", "note": "通道开关"},
        ],
        "resp": "+SETGPADCCHAN:X  (X:0-成功, 1-失败)",
        "example": "AT+SETGPADCCHAN=0,1",
    },
    {
        "name": "AT+GETGPADCVALUE", "group": "GPIO与ADC", "models": ["ALL"],
        "desc": "获取GPADC通道ADC值（满量程1023/10bit，内部参考1.8V，输入0~1.85V）。",
        "fmt": "AT+GETGPADCVALUE=X",
        "params": [{"name": "X", "range": "0-GPADC ch0, 1-GPADC ch1", "default": "0", "note": "ADC通道号"}],
        "resp": "+GETGPADCVALUE:X  (X:0~4096 ADC转换值)",
        "example": "AT+GETGPADCVALUE=0",
    },

    # ===================== 语音播报 =====================
    {
        "name": "AT+SETVASWITCH", "group": "语音播报", "models": ["ALL"],
        "desc": "语音播报开关设置。",
        "fmt": "AT+SETVASWITCH=X",
        "params": [{"name": "X", "range": "0-关闭, 1-开启", "default": "1", "note": "语音播报开关"}],
        "resp": "+SETVASWITCH:X  (X:0-成功, 1-失败)",
        "example": "AT+SETVASWITCH=1",
    },
    {
        "name": "AT+SETVALANGUAGE", "group": "语音播报", "models": ["ALL"],
        "desc": "语音播报语言设置。",
        "fmt": "AT+SETVALANGUAGE=X",
        "params": [{"name": "X", "range": "0-中文, 1-英文", "default": "0", "note": "播报语言"}],
        "resp": "+SETVALANGUAGE:X  (X:0-成功, 1-失败)",
        "example": "AT+SETVALANGUAGE=0",
    },
    {
        "name": "AT+SETVAGAIN", "group": "语音播报", "models": ["ALL"],
        "desc": "语音播报音量设置。",
        "fmt": "AT+SETVAGAIN=X",
        "params": [{"name": "X", "range": "0~5", "default": "5", "note": "语音播报音量等级"}],
        "resp": "+SETVAGAIN:X  (X:0-成功, 1-失败)",
        "example": "AT+SETVAGAIN=5",
    },

    # ===================== 省电与维护 =====================
    {
        "name": "AT+DMOSAVEPARAM", "group": "省电与维护", "models": ["ALL"],
        "desc": "保存校准参数到FLASH（AFC/RSSI等校准后务必发送，否则掉电丢失）。",
        "fmt": "AT+DMOSAVEPARAM",
        "params": [],
        "resp": "+DMOSAVEPARAM:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOSAVEPARAM",
    },
    {
        "name": "AT+DMOERASEPARAM", "group": "省电与维护", "models": ["ALL"],
        "desc": "擦除FLASH参数。",
        "fmt": "AT+DMOERASEPARAM=x",
        "params": [{"name": "x", "range": "擦除密码", "default": "2018777888", "note": "擦除密码"}],
        "resp": "+DMOERASEPARAM:X  (X:0-成功, 1-失败)",
        "example": "AT+DMOERASEPARAM=2018777888",
    },
    {
        "name": "AT+RESTOREFACTORYSET", "group": "省电与维护", "models": ["ALL"],
        "desc": "恢复出厂设置。",
        "fmt": "AT+RESTOREFACTORYSET=x",
        "params": [{"name": "x", "range": "恢复出厂密码", "default": "778123456", "note": "恢复密码"}],
        "resp": "+RESTOREFACTORYSET:X  (X:0-成功, 1-失败)",
        "example": "AT+RESTOREFACTORYSET=778123456",
    },
    {
        "name": "AT+SETINTODEEPSLEEP", "group": "省电与维护", "models": ["AM6133"],
        "desc": "设置进入深度睡眠（仅 AM6133；串口中断唤醒）。",
        "fmt": "AT+SETINTODEEPSLEEP",
        "params": [],
        "resp": "+SETINTODEEPSLEEP:X  (X:0-成功, 1-失败)",
        "example": "AT+SETINTODEEPSLEEP",
    },

    # ===================== 天气与其它 =====================
    {
        "name": "AT+SETFORECAST", "group": "天气与其它", "models": ["AM6132"],
        "desc": "设置天气预报信道/频率（仅 AM6132）。",
        "fmt": "AT+SETFORECAST=X",
        "params": [{"name": "X", "range": "0-关闭, 134000000~174000000-天气预报频率", "default": "1", "note": "频率或0关闭"}],
        "resp": "+SETFORECAST:X  (X:0-成功, 1-失败)",
        "example": "AT+SETFORECAST=1",
    },
    {
        "name": "AT+GETFORECASTSTATUS", "group": "天气与其它", "models": ["AM6132"],
        "desc": "接收到天气预报前导1050Hz信号时主动上报（仅 AM6132）。",
        "fmt": "(模块主动上报)",
        "params": [],
        "resp": "+GETFORECASTSTATUS:X  (X:1 预留)",
        "example": "(收到前导信号自动上报 +GETFORECASTSTATUS:1)",
    },
    {
        "name": "AT+SETDTMF", "group": "天气与其它", "models": ["ALL"],
        "desc": "设置DTMF时长及时间间隔。",
        "fmt": "AT+SETDTMF=x1,x2,x3,x4,x5,x6",
        "params": [
            {"name": "x1", "range": "1-DTMF1,2-DTMF2,3-DTMF3,4-DTMF4", "default": "1", "note": "DTMF系统编号"},
            {"name": "x2", "range": "0-侧音关, 1-侧音启用", "default": "0", "note": "侧音"},
            {"name": "x3", "range": "0~990 (步进15, ms) 预置时间", "default": "30", "note": "预置时间"},
            {"name": "x4", "range": "30~1890 (步进15, ms) 单码持续", "default": "90", "note": "单码持续时间"},
            {"name": "x5", "range": "30~1890 (步进15, ms) 码间间隔", "default": "180", "note": "码间间隔"},
            {"name": "x6", "range": "200~33000 (步进200, ms) 重置时间", "default": "1000", "note": "重置时间"},
        ],
        "resp": "+SETDTMF:X  (X:0-成功, 1-失败)",
        "example": "AT+SETDTMF=1,0,30,90,180,1000",
    },
    {
        "name": "AT+SETHOSTBAUDRATE", "group": "天气与其它", "models": ["AM6142"],
        "desc": "设置模块波特率（仅华安芯 AM6142）。",
        "fmt": "AT+SETHOSTBAUDRATE:X",
        "params": [{"name": "X", "range": "2400,4800,9600,14400,19200,28800,33600,38400,57600,115200,230400,460800,921600,1843200", "default": "9600", "note": "波特率"}],
        "resp": "+SETHOSTBAUDRATE:X  (X:0-成功, 1-失败)",
        "example": "AT+SETHOSTBAUDRATE:9600",
    },
]


def get_commands_by_group():
    """返回 {group: [commands...]}，仅包含 GROUPS 中定义的顺序。"""
    result = {g: [] for g in GROUPS}
    for c in COMMANDS:
        result.setdefault(c["group"], []).append(c)
    return result


def is_command_for_model(cmd, model):
    """判断指令是否适用于所选型号。"""
    if model == "通用(ALL)":
        return True
    models = cmd.get("models", ["ALL"])
    if "ALL" in models:
        return True
    return model in models


if __name__ == "__main__":
    print(f"共录入指令: {len(COMMANDS)} 条")
    for g, cmds in get_commands_by_group().items():
        print(f"  {g}: {len(cmds)} 条")
