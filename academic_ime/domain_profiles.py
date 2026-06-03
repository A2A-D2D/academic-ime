"""Domain-specific word profiles for AcademicIME.

Each domain has an id, name, description, and a list of (word, rank) tuples.
Higher priority domains get weight multipliers during lexicon building.
"""

from __future__ import annotations

from typing import TypedDict


class DomainProfile(TypedDict):
    id: str
    name: str
    icon: str
    description: str
    words: list[tuple[str, int]]


DOMAINS: dict[str, DomainProfile] = {
    "diplomacy": {
        "id": "diplomacy",
        "name": "外交 / 国际关系",
        "icon": "🌐",
        "description": "国际政治、外交文书、条约协议、国际组织等专业术语",
        "words": [
            # International Organizations
            ("United-Nations", 1), ("UN", 2), ("Security-Council", 3), ("General-Assembly", 4),
            ("WHO", 5), ("WTO", 6), ("IMF", 7), ("World-Bank", 8), ("NATO", 9),
            ("European-Union", 10), ("ASEAN", 11), ("APEC", 12), ("OPEC", 13),
            ("UNESCO", 14), ("UNICEF", 15), ("ICJ", 16), ("ICC", 17), ("IEA", 18),
            ("G20", 19), ("G7", 20), ("BRICS", 21), ("SCO", 22), ("OECD", 23),
            # Diplomatic Terms
            ("diplomacy", 24), ("diplomatic", 25), ("treaty", 26), ("agreement", 27),
            ("memorandum", 28), ("communique", 29), ("declaration", 30), ("resolution", 31),
            ("sanction", 32), ("embargo", 33), ("summit", 34), ("bilateral", 35),
            ("multilateral", 36), ("unilateral", 37), ("consensus", 38), ("veto", 39),
            ("ratification", 40), ("accession", 41), ("protocol", 42), ("convention", 43),
            ("charter", 44), ("mandate", 45), ("jurisdiction", 46), ("territorial", 47),
            ("sovereignty", 48), ("non-interference", 49), ("peacekeeping", 50), ("mediation", 51),
            ("arbitration", 52), ("negotiation", 53), ("dialogue", 54), ("detente", 55),
            ("rapprochement", 56), ("alliance", 57), ("coalition", 58), ("partnership", 59),
            ("strategic", 60), ("geopolitical", 61), ("geopolitics", 62), ("foreign-policy", 63),
            ("international-relations", 64), ("global-governance", 65), ("soft-power", 66), ("hard-power", 67),
            ("public-diplomacy", 68), ("track-two", 69), ("confidence-building", 70),
            # Key Countries / Regions
            ("United-States", 71), ("China", 72), ("Russia", 73), ("Japan", 74),
            ("India", 75), ("Germany", 76), ("France", 77), ("United-Kingdom", 78),
            ("Middle-East", 79), ("Asia-Pacific", 80), ("Indo-Pacific", 81), ("Global-South", 82),
            # Chinese diplomatic terms
            ("一带一路", 83), ("人类命运共同体", 84), ("和平共处五项原则", 85), ("独立自主", 86),
            ("和平发展", 87), ("互利共赢", 88), ("合作共赢", 89), ("对话协商", 90),
            ("全球安全倡议", 91), ("全球发展倡议", 92), ("全球文明倡议", 93), ("新型国际关系", 94),
            ("多边主义", 95), ("单边主义", 96), ("保护主义", 97), ("零和博弈", 98),
            ("战略伙伴关系", 99), ("全面战略伙伴", 100), ("外交政策", 101), ("国际法", 102),
            ("主权", 103), ("领土完整", 104), ("内政", 105), ("不干涉", 106),
            ("制裁", 107), ("禁运", 108), ("最惠国待遇", 109), ("引渡", 110),
            ("斡旋", 111), ("调停", 112), ("缔约", 113), ("协定", 114),
            ("宪章", 115), ("框架协议", 116), ("谅解备忘录", 117), ("联合声明", 118),
            ("安理会", 119), ("常任理事国", 120),
        ],
    },
    "legal": {
        "id": "legal",
        "name": "法律 / 政策",
        "icon": "⚖️",
        "description": "法律法规、司法程序、政策分析、合规监管等专业术语",
        "words": [
            # Legal English
            ("legislation", 1), ("regulation", 2), ("statute", 3), ("ordinance", 4),
            ("decree", 5), ("directive", 6), ("constitution", 7), ("amendment", 8),
            ("judicial", 9), ("judiciary", 10), ("jurisdiction", 11), ("jurisprudence", 12),
            ("precedent", 13), ("ruling", 14), ("verdict", 15), ("judgment", 16),
            ("litigation", 17), ("arbitration", 18), ("mediation", 19), ("conciliation", 20),
            ("plaintiff", 21), ("defendant", 22), ("appellant", 23), ("respondent", 24),
            ("prosecutor", 25), ("defense-attorney", 26), ("counsel", 27), ("solicitor", 28),
            ("barrister", 29), ("notary", 30), ("affidavit", 31), ("testimony", 32),
            ("subpoena", 33), ("warrant", 34), ("indictment", 35), ("conviction", 36),
            ("acquittal", 37), ("appeal", 38), ("remand", 39), ("injunction", 40),
            ("liability", 41), ("negligence", 42), ("tort", 43), ("damages", 44),
            ("compensation", 45), ("indemnity", 46), ("warranty", 47), ("guarantee", 48),
            ("contract", 49), ("terms-and-conditions", 50), ("force-majeure", 51), ("breach", 52),
            ("termination", 53), ("severability", 54), ("null-and-void", 55), ("enforceability", 56),
            ("intellectual-property", 57), ("copyright", 58), ("trademark", 59), ("patent", 60),
            ("trade-secret", 61), ("infringement", 62), ("licensing", 63), ("royalty", 64),
            ("compliance", 65), ("due-diligence", 66), ("anti-trust", 67), ("anti-corruption", 68),
            ("anti-money-laundering", 69), ("data-privacy", 70), ("GDPR", 71), ("CCPA", 72),
            ("whistleblower", 73), ("ombudsman", 74), ("administrative-review", 75),
            ("policy-analysis", 76), ("regulatory-impact", 77), ("legislative", 78), ("executive-order", 79),
            # Chinese legal terms
            ("法律", 80), ("法规", 81), ("条例", 82), ("规章", 83),
            ("司法解释", 84), ("最高人民法院", 85), ("仲裁委员会", 86), ("行政复议", 87),
            ("行政诉讼", 88), ("民事诉讼", 89), ("刑事诉讼", 90), ("公益诉讼", 91),
            ("知识产权", 92), ("专利法", 93), ("商标法", 94), ("著作权", 95),
            ("合同法", 96), ("公司法", 97), ("劳动法", 98), ("税法", 99),
            ("证券法", 100), ("反垄断", 101), ("反不正当竞争", 102), ("消费者权益", 103),
            ("个人信息保护", 104), ("数据安全", 105), ("网络安全", 106), ("合规审查", 107),
            ("尽职调查", 108), ("法律意见书", 109), ("裁判文书", 110), ("判决", 111),
            ("裁定", 112), ("调解", 113), ("和解", 114), ("起诉", 115),
            ("应诉", 116), ("答辩", 117), ("上诉", 118), ("再审", 119),
            ("执行", 120),
        ],
    },
    "cs_chip": {
        "id": "cs_chip",
        "name": "计算机 / 芯片",
        "icon": "💻",
        "description": "半导体设计、集成电路、处理器架构、EDA工具、算法等专业术语",
        "words": [
            # Semiconductor / Chip
            ("semiconductor", 1), ("integrated-circuit", 2), ("ASIC", 3), ("FPGA", 4),
            ("SoC", 5), ("CPU", 6), ("GPU", 7), ("TPU", 8), ("NPU", 9),
            ("DSP", 10), ("MCU", 11), ("RISC-V", 12), ("ARM", 13), ("x86", 14),
            ("wafer", 15), ("lithography", 16), ("EUV", 17), ("DUV", 18),
            ("FinFET", 19), ("GAA", 20), ("nanosheet", 21), ("CMOS", 22),
            ("silicon", 23), ("germanium", 24), ("substrate", 25), ("doping", 26),
            ("fabrication", 27), ("foundry", 28), ("tape-out", 29), ("tapeout", 30),
            ("yield", 31), ("defect-density", 32), ("process-node", 33), ("nm-process", 34),
            ("standard-cell", 35), ("macro-cell", 36), ("IP-core", 37), ("synthesis", 38),
            ("place-and-route", 39), ("floorplanning", 40), ("clock-tree", 41), ("timing-closure", 42),
            ("verification", 43), ("simulation", 44), ("emulation", 45), ("formal-verification", 46),
            ("DFT", 47), ("scan-chain", 48), ("BIST", 49), ("JTAG", 50),
            ("SRAM", 51), ("DRAM", 52), ("flash-memory", 53), ("NAND", 54),
            ("NOR", 55), ("eMMC", 56), ("UFS", 57), ("PCIe", 58),
            ("DDR", 59), ("HBM", 60), ("SerDes", 61), ("PHY", 62),
            ("PLL", 63), ("DLL", 64), ("ADC", 65), ("DAC", 66),
            ("PMIC", 67), ("LDO", 68), ("DC-DC", 69), ("ESD", 70),
            ("signal-integrity", 71), ("power-integrity", 72), ("EMC", 73), ("EMI", 74),
            ("thermal", 75), ("cooling", 76), ("package", 77), ("interposer", 78),
            ("chiplets", 79), ("3D-IC", 80), ("through-silicon-via", 81),
            # EDA / Tools
            ("EDA", 82), ("synthesis-tool", 83), ("static-timing-analysis", 84), ("power-analysis", 85),
            ("DRC", 86), ("LVS", 87), ("parasitic-extraction", 88), ("SPICE", 89),
            # Chinese chip terms
            ("半导体", 90), ("集成电路", 91), ("晶圆", 92), ("光刻", 93),
            ("流片", 94), ("量产", 95), ("良率", 96), ("工艺节点", 97),
            ("功耗", 98), ("时序", 99), ("版图设计", 100), ("物理设计", 101),
            ("综合优化", 102), ("布局布线", 103), ("时钟树综合", 104), ("时序收敛", 105),
            ("形式验证", 106), ("可测试性设计", 107), ("封装测试", 108), ("信号完整性", 109),
            ("电源完整性", 110), ("热管理", 111), ("静电防护", 112), ("可靠性", 113),
            ("微架构", 114), ("指令集", 115), ("流水线", 116), ("缓存一致性", 117),
            ("乱序执行", 118), ("分支预测", 119), ("超标量", 120),
        ],
    },
    "medical_bio": {
        "id": "medical_bio",
        "name": "医学 / 生物",
        "icon": "🧬",
        "description": "临床医学、生物医药、基因技术、医疗器械等专业术语",
        "words": [
            # Medical English
            ("diagnosis", 1), ("prognosis", 2), ("etiology", 3), ("pathogenesis", 4),
            ("pathology", 5), ("physiology", 6), ("anatomy", 7), ("histology", 8),
            ("clinical", 9), ("therapeutic", 10), ("pharmacology", 11), ("pharmacokinetics", 12),
            ("bioavailability", 13), ("half-life", 14), ("dosing", 15), ("titration", 16),
            ("efficacy", 17), ("adverse-event", 18), ("contraindication", 19), ("placebo", 20),
            ("randomized-controlled-trial", 21), ("double-blind", 22), ("meta-analysis", 23), ("cohort-study", 24),
            ("systematic-review", 25), ("evidence-based", 26), ("clinical-guideline", 27), ("standard-of-care", 28),
            ("informed-consent", 29), ("IRB", 30), ("ethics-committee", 31), ("HIPAA", 32),
            ("epidemiology", 33), ("incidence", 34), ("prevalence", 35), ("mortality", 36),
            ("morbidity", 37), ("comorbidity", 38), ("risk-factor", 39), ("odds-ratio", 40),
            ("biomarker", 41), ("screening", 42), ("prevention", 43), ("intervention", 44),
            ("cardiology", 45), ("neurology", 46), ("oncology", 47), ("hematology", 48),
            ("immunology", 49), ("endocrinology", 50), ("gastroenterology", 51), ("nephrology", 52),
            ("pulmonology", 53), ("rheumatology", 54), ("dermatology", 55), ("ophthalmology", 56),
            ("radiology", 57), ("pathology", 58), ("anesthesiology", 59), ("emergency-medicine", 60),
            ("intensive-care", 61), ("surgery", 62), ("medical-device", 63), ("implant", 64),
            # Biology / Genetics
            ("genome", 65), ("genomics", 66), ("proteomics", 67), ("transcriptomics", 68),
            ("metabolomics", 69), ("CRISPR", 70), ("gene-editing", 71), ("gene-therapy", 72),
            ("mRNA", 73), ("DNA", 74), ("RNA", 75), ("protein", 76),
            ("enzyme", 77), ("receptor", 78), ("ligand", 79), ("antibody", 80),
            ("monoclonal-antibody", 81), ("immunotherapy", 82), ("cell-therapy", 83), ("CAR-T", 84),
            ("stem-cell", 85), ("regenerative-medicine", 86), ("tissue-engineering", 87), ("organoid", 88),
            ("microbiome", 89), ("virology", 90), ("bacteria", 91), ("virus", 92),
            ("vaccine", 93), ("clinical-trial", 94), ("FDA", 95), ("NMPA", 96),
            ("pharmaceutical", 97), ("drug-discovery", 98), ("drug-development", 99), ("biotech", 100),
            # Chinese medical terms
            ("诊断", 101), ("治疗", 102), ("预后", 103), ("病因", 104),
            ("病理", 105), ("生理", 106), ("临床", 107), ("药学", 108),
            ("随机对照", 109), ("双盲试验", 110), ("系统综述", 111), ("循证医学", 112),
            ("流行病学", 113), ("发病率", 114), ("死亡率", 115), ("危险因素", 116),
            ("基因组", 117), ("蛋白质组", 118), ("基因编辑", 119), ("免疫治疗", 120),
        ],
    },
    "finance": {
        "id": "finance",
        "name": "金融 / 经济",
        "icon": "📈",
        "description": "投资银行、证券交易、宏观经济、风险管理等专业术语",
        "words": [
            # Finance English
            ("macroeconomics", 1), ("microeconomics", 2), ("fiscal-policy", 3), ("monetary-policy", 4),
            ("inflation", 5), ("deflation", 6), ("stagflation", 7), ("recession", 8),
            ("GDP", 9), ("CPI", 10), ("PPI", 11), ("PMI", 12),
            ("interest-rate", 13), ("benchmark-rate", 14), ("federal-funds-rate", 15), ("LIBOR", 16),
            ("exchange-rate", 17), ("foreign-exchange", 18), ("currency", 19), ("depreciation", 20),
            ("appreciation", 21), ("balance-of-payments", 22), ("trade-deficit", 23), ("current-account", 24),
            ("equity", 25), ("fixed-income", 26), ("bond", 27), ("treasury", 28),
            ("corporate-bond", 29), ("yield", 30), ("yield-curve", 31), ("duration", 32),
            ("stock", 33), ("dividend", 34), ("market-cap", 35), ("P/E-ratio", 36),
            ("IPO", 37), ("secondary-offering", 38), ("private-placement", 39), ("underwriter", 40),
            ("mergers-and-acquisitions", 41), ("acquisition", 42), ("leveraged-buyout", 43), ("due-diligence", 44),
            ("valuation", 45), ("DCF", 46), ("EBITDA", 47), ("net-present-value", 48),
            ("internal-rate-of-return", 49), ("ROI", 50), ("ROE", 51), ("beta-coefficient", 52),
            ("portfolio", 53), ("asset-allocation", 54), ("diversification", 55), ("hedging", 56),
            ("derivatives", 57), ("options", 58), ("futures", 59), ("swap", 60),
            ("hedge-fund", 61), ("private-equity", 62), ("venture-capital", 63), ("angel-investor", 64),
            ("fintech", 65), ("blockchain", 66), ("cryptocurrency", 67), ("Bitcoin", 68),
            ("DeFi", 69), ("NFT", 70), ("stablecoin", 71), ("smart-contract", 72),
            ("risk-management", 73), ("VaR", 74), ("stress-testing", 75), ("credit-risk", 76),
            ("market-risk", 77), ("operational-risk", 78), ("liquidity", 79), ("solvency", 80),
            ("compliance", 81), ("Basel", 82), ("capital-adequacy", 83), ("stress-test", 84),
            ("quantitative-easing", 85), ("quantitative-tightening", 86), ("balance-sheet", 87), ("financial-stability", 88),
            # Chinese finance terms
            ("宏观经济", 89), ("货币政策", 90), ("财政政策", 91), ("通货膨胀", 92),
            ("汇率", 93), ("利率", 94), ("国内生产总值", 95), ("消费者价格指数", 96),
            ("上证指数", 97), ("深证成指", 98), ("创业板", 99), ("科创板", 100),
            ("北交所", 101), ("注册制", 102), ("信息披露", 103), ("内幕交易", 104),
            ("量化宽松", 105), ("降息", 106), ("加息", 107), ("存款准备金", 108),
            ("不良贷款", 109), ("杠杆率", 110), ("系统性风险", 111), ("影子银行", 112),
            ("数字货币", 113), ("跨境支付", 114), ("外汇储备", 115), ("人民币国际化", 116),
            ("碳交易", 117), ("绿色金融", 118), ("普惠金融", 119), ("供应链金融", 120),
        ],
    },
    "gaming": {
        "id": "gaming",
        "name": "游戏 / 娱乐",
        "icon": "🎮",
        "description": "游戏设计、电竞、二次元、影视动漫等流行文化术语",
        "words": [
            # Gaming English
            ("gameplay", 1), ("game-mechanics", 2), ("level-design", 3), ("world-building", 4),
            ("open-world", 5), ("sandbox", 6), ("roguelike", 7), ("roguelite", 8),
            ("soulslike", 9), ("metroidvania", 10), ("FPS", 11), ("TPS", 12),
            ("RPG", 13), ("MMORPG", 14), ("MOBA", 15), ("RTS", 16),
            ("battle-royale", 17), ("survival", 18), ("crafting", 19), ("procedural-generation", 20),
            ("NPC", 21), ("boss-fight", 22), ("quest", 23), ("achievement", 24),
            ("loot", 25), ("grinding", 26), ("progression", 27), ("skill-tree", 28),
            ("DLC", 29), ("expansion", 30), ("season-pass", 31), ("battle-pass", 32),
            ("microtransaction", 33), ("gacha", 34), ("free-to-play", 35), ("pay-to-win", 36),
            ("esports", 37), ("competitive", 38), ("ranked", 39), ("ELO", 40),
            ("tournament", 41), ("championship", 42), ("LAN-party", 43), ("streaming", 44),
            ("Twitch", 45), ("speedrun", 46), ("TAS", 47), ("modding", 48),
            ("indie-game", 49), ("AAA-game", 50), ("remake", 51), ("remaster", 52),
            ("cross-platform", 53), ("cloud-gaming", 54), ("VR", 55), ("AR", 56),
            ("haptic-feedback", 57), ("ray-tracing", 58), ("frame-rate", 59), ("input-lag", 60),
            ("Steam", 61), ("Epic-Games", 62), ("Xbox-Game-Pass", 63), ("PlayStation", 64),
            ("Nintendo", 65), ("Unreal-Engine", 66), ("Unity", 67),
            # Entertainment
            ("anime", 68), ("manga", 69), ("cosplay", 70), ("otaku", 71),
            ("OVA", 72), ("light-novel", 73), ("visual-novel", 74), ("doujin", 75),
            ("VTuber", 76), ("hololive", 77), ("streamer", 78), ("creator", 79),
            # Chinese gaming terms
            ("游戏设计", 80), ("开放世界", 81), ("角色扮演", 82), ("第一人称", 83),
            ("多人联机", 84), ("竞技排位", 85), ("电子竞技", 86), ("电竞赛事", 87),
            ("赛季", 88), ("段位", 89), ("排位赛", 90), ("匹配机制", 91),
            ("抽卡", 92), ("氪金", 93), ("肝", 94), ("欧皇", 95),
            ("单机", 96), ("联机", 97), ("手柄", 98), ("键鼠", 99),
            ("帧率", 100), ("延迟", 101), ("优化", 102), ("画质", 103),
            ("二次元", 104), ("番剧", 105), ("周边", 106), ("手办", 107),
            ("模型", 108), ("桌游", 109), ("剧本杀", 110), ("密室逃脱", 111),
            ("盲盒", 112), ("限定", 113), ("联动", 114), ("复刻", 115),
            ("版本更新", 116), ("活动", 117), ("签到", 118), ("通行证", 119),
            ("成就", 120),
        ],
    },
    "daily": {
        "id": "daily",
        "name": "日常用语",
        "icon": "📝",
        "description": "办公沟通、邮件写作、日程安排、日常聊天等高频词汇",
        "words": [
            # Office / Communication
            ("meeting", 1), ("agenda", 2), ("minutes", 3), ("action-item", 4),
            ("deadline", 5), ("timeline", 6), ("milestone", 7), ("deliverable", 8),
            ("stakeholder", 9), ("alignment", 10), ("sync", 11), ("standup", 12),
            ("kickoff", 13), ("retrospective", 14), ("brainstorm", 15), ("workshop", 16),
            ("seminar", 17), ("conference", 18), ("webinar", 19), ("presentation", 20),
            ("slides", 21), ("deck", 22), ("handout", 23), ("memo", 24),
            ("report", 25), ("draft", 26), ("outline", 27), ("template", 28),
            ("proposal", 29), ("budget", 30), ("expense", 31), ("reimbursement", 32),
            ("invoice", 33), ("payment", 34), ("contract", 35), ("agreement", 36),
            ("email", 37), ("subject-line", 38), ("attachment", 39), ("forward", 40),
            ("reply-all", 41), ("BCC", 42), ("newsletter", 43), ("subscription", 44),
            ("KPI", 45), ("OKR", 46), ("SLA", 47), ("quarterly-review", 48),
            ("performance-review", 49), ("onboarding", 50), ("offboarding", 51), ("announcement", 52),
            ("reminder", 53), ("follow-up", 54), ("FYI", 55), ("ASAP", 56),
            ("TBD", 57), ("TBA", 58), ("ETA", 59), ("EOD", 60),
            # Daily Life
            ("schedule", 61), ("calendar", 62), ("appointment", 63), ("reservation", 64),
            ("booking", 65), ("check-in", 66), ("checkout", 67), ("itinerary", 68),
            ("commute", 69), ("traffic", 70), ("parking", 71), ("directions", 72),
            ("shopping", 73), ("delivery", 74), ("coupon", 75), ("discount", 76),
            ("refund", 77), ("exchange", 78), ("warranty", 79), ("receipt", 80),
            ("menu", 81), ("recipe", 82), ("ingredient", 83), ("nutrition", 84),
            ("fitness", 85), ("workout", 86), ("cardio", 87), ("meditation", 88),
            ("weather", 89), ("temperature", 90), ("humidity", 91), ("forecast", 92),
            # Chinese daily terms
            ("会议", 93), ("日程", 94), ("截止日期", 95), ("里程碑", 96),
            ("周报", 97), ("月报", 98), ("季度总结", 99), ("绩效评估", 100),
            ("邮件", 101), ("附件", 102), ("抄送", 103), ("密送", 104),
            ("回复全部", 105), ("请假", 106), ("出差", 107), ("报销", 108),
            ("签到", 109), ("打卡", 110), ("加班", 111), ("调休", 112),
            ("通知", 113), ("公告", 114), ("提醒", 115), ("待办", 116),
            ("快递", 117), ("外卖", 118), ("导航", 119), ("出行", 120),
        ],
    },
    "accounting": {
        "id": "accounting",
        "name": "会计 / 审计",
        "icon": "🧾",
        "description": "财务会计、审计核查、税务筹划、财务报表等专业术语",
        "words": [
            # Accounting English
            ("accounting", 1), ("financial-reporting", 2), ("GAAP", 3), ("IFRS", 4),
            ("balance-sheet", 5), ("income-statement", 6), ("cash-flow", 7), ("statement", 8),
            ("general-ledger", 9), ("trial-balance", 10), ("journal-entry", 11), ("double-entry", 12),
            ("debit", 13), ("credit", 14), ("accrual", 15), ("deferral", 16),
            ("depreciation", 17), ("amortization", 18), ("impairment", 19), ("write-off", 20),
            ("accounts-receivable", 21), ("accounts-payable", 22), ("aging-report", 23), ("reconciliation", 24),
            ("bank-reconciliation", 25), ("intercompany", 26), ("consolidation", 27), ("elimination", 28),
            ("revenue-recognition", 29), ("matching-principle", 30), ("materiality", 31), ("disclosure", 32),
            ("audit", 33), ("auditor", 34), ("internal-audit", 35), ("external-audit", 36),
            ("audit-opinion", 37), ("unqualified-opinion", 38), ("qualified-opinion", 39), ("going-concern", 40),
            ("substantive-procedure", 41), ("test-of-controls", 42), ("sampling-risk", 43), ("material-misstatement", 44),
            ("internal-control", 45), ("SOX", 46), ("COSO", 47), ("risk-assessment", 48),
            ("fraud", 49), ("forensic-accounting", 50), ("compliance", 51), ("regulatory-filing", 52),
            ("tax", 53), ("taxation", 54), ("VAT", 55), ("GST", 56),
            ("corporate-tax", 57), ("income-tax", 58), ("withholding-tax", 59), ("transfer-pricing", 60),
            ("tax-return", 61), ("tax-audit", 62), ("deduction", 63), ("exemption", 64),
            ("deferred-tax", 65), ("tax-provision", 66), ("payroll", 67), ("payroll-tax", 68),
            ("cost-accounting", 69), ("activity-based-costing", 70), ("standard-costing", 71), ("variance-analysis", 72),
            ("budgeting", 73), ("forecasting", 74), ("financial-planning", 75), ("capital-budgeting", 76),
            ("working-capital", 77), ("liquidity-ratio", 78), ("current-ratio", 79), ("quick-ratio", 80),
            ("debt-to-equity", 81), ("return-on-assets", 82), ("return-on-equity", 83), ("gross-margin", 84),
            ("net-income", 85), ("EBIT", 86), ("EBITDA", 87), ("free-cash-flow", 88),
            ("financial-analysis", 89), ("ratio-analysis", 90), ("benchmarking", 91), ("KPI", 92),
            ("ERP", 93), ("SAP", 94), ("Oracle-Financials", 95), ("QuickBooks", 96),
            ("bookkeeping", 97), ("invoice", 98), ("receipt", 99), ("voucher", 100),
            # Chinese accounting terms
            ("会计", 101), ("财务报告", 102), ("资产负债表", 103), ("利润表", 104),
            ("现金流量表", 105), ("总账", 106), ("明细账", 107), ("凭证", 108),
            ("借贷", 109), ("折旧", 110), ("摊销", 111), ("坏账", 112),
            ("应收账款", 113), ("应付账款", 114), ("银行对账", 115), ("关联交易", 116),
            ("合并报表", 117), ("收入确认", 118), ("审计", 119), ("内审", 120),
        ],
    },
    "education": {
        "id": "education",
        "name": "教育 / 心理",
        "icon": "🎓",
        "description": "教育学、心理学、课程设计、认知科学等专业术语",
        "words": [
            # Education English
            ("education", 1), ("pedagogy", 2), ("andragogy", 3), ("curriculum", 4),
            ("syllabus", 5), ("lesson-plan", 6), ("instructional-design", 7), ("learning-objective", 8),
            ("assessment", 9), ("formative-assessment", 10), ("summative-assessment", 11), ("rubric", 12),
            ("competency-based", 13), ("outcome-based", 14), ("student-centered", 15), ("blended-learning", 16),
            ("e-learning", 17), ("MOOC", 18), ("LMS", 19), ("learning-management", 20),
            ("flipped-classroom", 21), ("active-learning", 22), ("collaborative-learning", 23), ("peer-assessment", 24),
            ("scaffolding", 25), ("differentiated-instruction", 26), ("inclusive-education", 27), ("special-education", 28),
            ("K-12", 29), ("higher-education", 30), ("vocational-education", 31), ("lifelong-learning", 32),
            ("accreditation", 33), ("enrollment", 34), ("graduation-rate", 35), ("dropout", 36),
            ("faculty", 37), ("adjunct", 38), ("tenure-track", 39), ("dissertation", 40),
            ("edtech", 41), ("gamification", 42), ("micro-credential", 43), ("badge", 44),
            # Psychology English
            ("psychology", 45), ("cognitive", 46), ("behavioral", 47), ("developmental", 48),
            ("social-psychology", 49), ("clinical-psychology", 50), ("neuropsychology", 51), ("psychiatry", 52),
            ("cognition", 53), ("perception", 54), ("attention", 55), ("memory", 56),
            ("learning-theory", 57), ("conditioning", 58), ("reinforcement", 59), ("motivation", 60),
            ("emotion", 61), ("personality", 62), ("temperament", 63), ("attachment", 64),
            ("mental-health", 65), ("wellbeing", 66), ("resilience", 67), ("mindfulness", 68),
            ("therapy", 69), ("CBT", 70), ("psychotherapy", 71), ("counseling", 72),
            ("DSM", 73), ("diagnosis", 74), ("intervention", 75), ("psychometrics", 76),
            ("IQ", 77), ("EQ", 78), ("aptitude", 79), ("assessment-tool", 80),
            ("bias", 81), ("stereotype", 82), ("prejudice", 83), ("discrimination", 84),
            ("growth-mindset", 85), ("self-efficacy", 86), ("self-regulation", 87), ("executive-function", 88),
            # Chinese education/psychology terms
            ("教育", 89), ("教学", 90), ("课程", 91), ("评估", 92),
            ("学习目标", 93), ("在线教育", 94), ("终身学习", 95), ("高等教育", 96),
            ("职业教育", 97), ("特殊教育", 98), ("教育公平", 99), ("因材施教", 100),
            ("心理学", 101), ("认知", 102), ("行为", 103), ("发展", 104),
            ("社会心理", 105), ("心理健康", 106), ("幸福感", 107), ("心理韧性", 108),
            ("动机", 109), ("情绪", 110), ("人格", 111), ("智力", 112),
            ("注意力", 113), ("记忆力", 114), ("学习障碍", 115), ("早期教育", 116),
            ("教师发展", 117), ("教育技术", 118), ("翻转课堂", 119), ("混合式教学", 120),
        ],
    },
    "architecture": {
        "id": "architecture",
        "name": "建筑 / 土木",
        "icon": "🏗️",
        "description": "建筑设计、土木工程、结构力学、城市规划等专业术语",
        "words": [
            # Architecture / Civil English
            ("architecture", 1), ("architectural-design", 2), ("urban-planning", 3), ("city-planning", 4),
            ("zoning", 5), ("land-use", 6), ("master-plan", 7), ("site-plan", 8),
            ("structural", 9), ("foundation", 10), ("footing", 11), ("pile-foundation", 12),
            ("load-bearing", 13), ("dead-load", 14), ("live-load", 15), ("seismic-load", 16),
            ("reinforced-concrete", 17), ("prestressed-concrete", 18), ("steel-structure", 19), ("composite", 20),
            ("beam", 21), ("column", 22), ("slab", 23), ("truss", 24),
            ("cantilever", 25), ("shear-wall", 26), ("moment-frame", 27), ("bracing", 28),
            ("finite-element", 29), ("structural-analysis", 30), ("deflection", 31), ("buckling", 32),
            ("geotechnical", 33), ("soil-mechanics", 34), ("bearing-capacity", 35), ("settlement", 36),
            ("excavation", 37), ("retaining-wall", 38), ("tunnel", 39), ("bridge", 40),
            ("highway", 41), ("pavement", 42), ("asphalt", 43), ("drainage", 44),
            ("hydraulics", 45), ("hydrology", 46), ("water-supply", 47), ("wastewater", 48),
            ("HVAC", 49), ("plumbing", 50), ("electrical", 51), ("fire-protection", 52),
            ("BIM", 53), ("CAD", 54), ("Revit", 55), ("AutoCAD", 56),
            ("sustainability", 57), ("LEED", 58), ("green-building", 59), ("energy-efficiency", 60),
            ("facade", 61), ("curtain-wall", 62), ("cladding", 63), ("glazing", 64),
            ("interior-design", 65), ("landscape", 66), ("spatial", 67), ("acoustics", 68),
            ("construction", 69), ("contractor", 70), ("subcontractor", 71), ("project-management", 72),
            ("cost-estimation", 73), ("quantity-survey", 74), ("specification", 75), ("building-code", 76),
            ("permit", 77), ("inspection", 78), ("occupancy", 79), ("certificate", 80),
            # Chinese architecture terms
            ("建筑", 81), ("设计", 82), ("结构", 83), ("基础", 84),
            ("地基", 85), ("桩基", 86), ("钢筋混凝土", 87), ("钢结构", 88),
            ("梁", 89), ("柱", 90), ("板", 91), ("剪力墙", 92),
            ("有限元分析", 93), ("抗震", 94), ("岩土", 95), ("隧道", 96),
            ("桥梁", 97), ("公路", 98), ("市政", 99), ("给排水", 100),
            ("暖通", 101), ("消防", 102), ("绿色建筑", 103), ("节能", 104),
            ("城市规划", 105), ("用地", 106), ("总规", 107), ("控规", 108),
            ("修规", 109), ("景观", 110), ("室内", 111), ("幕墙", 112),
            ("施工", 113), ("监理", 114), ("造价", 115), ("工程量清单", 116),
            ("招投标", 117), ("竣工验收", 118), ("容积率", 119), ("建筑密度", 120),
        ],
    },
    "mechanical": {
        "id": "mechanical",
        "name": "机械 / 汽车",
        "icon": "⚙️",
        "description": "机械设计、汽车工程、制造工艺、自动化控制等专业术语",
        "words": [
            # Mechanical / Automotive English
            ("mechanical", 1), ("mechanics", 2), ("dynamics", 3), ("kinematics", 4),
            ("statics", 5), ("vibration", 6), ("fatigue", 7), ("fracture", 8),
            ("stress-analysis", 9), ("strain", 10), ("deformation", 11), ("elasticity", 12),
            ("plasticity", 13), ("creep", 14), ("hardness", 15), ("toughness", 16),
            ("tensile", 17), ("compressive", 18), ("shear", 19), ("torsion", 20),
            ("bearing", 21), ("gear", 22), ("shaft", 23), ("coupling", 24),
            ("clutch", 25), ("brake", 26), ("seal", 27), ("gasket", 28),
            ("lubrication", 29), ("tribology", 30), ("wear", 31), ("friction", 32),
            ("hydraulic", 33), ("pneumatic", 34), ("actuator", 35), ("valve", 36),
            ("pump", 37), ("compressor", 38), ("turbine", 39), ("engine", 40),
            ("combustion", 41), ("internal-combustion", 42), ("diesel", 43), ("gasoline", 44),
            ("electric-vehicle", 45), ("EV", 46), ("hybrid", 47), ("battery", 48),
            ("powertrain", 49), ("transmission", 50), ("drivetrain", 51), ("chassis", 52),
            ("suspension", 53), ("steering", 54), ("braking-system", 55), ("ABS", 56),
            ("autonomous", 57), ("ADAS", 58), ("lidar", 59), ("radar", 60),
            ("manufacturing", 61), ("machining", 62), ("CNC", 63), ("milling", 64),
            ("turning", 65), ("grinding", 66), ("welding", 67), ("casting", 68),
            ("forging", 69), ("stamping", 70), ("injection-molding", 71), ("additive-manufacturing", 72),
            ("3D-printing", 73), ("quality-control", 74), ("tolerance", 75), ("GD&T", 76),
            ("lean-manufacturing", 77), ("Six-Sigma", 78), ("FMEA", 79), ("PPAP", 80),
            # Chinese mechanical terms
            ("机械", 81), ("力学", 82), ("动力学", 83), ("静力学", 84),
            ("振动", 85), ("疲劳", 86), ("断裂", 87), ("应力", 88),
            ("应变", 89), ("弹性", 90), ("塑性", 91), ("硬度", 92),
            ("轴承", 93), ("齿轮", 94), ("轴", 95), ("联轴器", 96),
            ("离合器", 97), ("制动器", 98), ("密封", 99), ("润滑", 100),
            ("液压", 101), ("气动", 102), ("阀门", 103), ("泵", 104),
            ("压缩机", 105), ("汽轮机", 106), ("发动机", 107), ("内燃机", 108),
            ("电动车", 109), ("混合动力", 110), ("动力总成", 111), ("变速箱", 112),
            ("底盘", 113), ("悬挂", 114), ("转向", 115), ("制动", 116),
            ("自动驾驶", 117), ("传感器", 118), ("激光雷达", 119), ("毫米波雷达", 120),
        ],
    },
    "chemistry": {
        "id": "chemistry",
        "name": "化学 / 材料",
        "icon": "🧪",
        "description": "化学合成、材料科学、化工工艺、分析检测等专业术语",
        "words": [
            # Chemistry / Materials English
            ("chemistry", 1), ("chemical", 2), ("organic", 3), ("inorganic", 4),
            ("analytical", 5), ("physical-chemistry", 6), ("biochemistry", 7), ("polymer", 8),
            ("synthesis", 9), ("catalysis", 10), ("catalyst", 11), ("enzyme", 12),
            ("reaction", 13), ("reagent", 14), ("solvent", 15), ("solution", 16),
            ("concentration", 17), ("molarity", 18), ("pH", 19), ("titration", 20),
            ("chromatography", 21), ("HPLC", 22), ("GC-MS", 23), ("spectroscopy", 24),
            ("NMR", 25), ("XRD", 26), ("FTIR", 27), ("mass-spectrometry", 28),
            ("distillation", 29), ("extraction", 30), ("crystallization", 31), ("precipitation", 32),
            ("oxidation", 33), ("reduction", 34), ("redox", 35), ("electrochemistry", 36),
            ("electrolysis", 37), ("corrosion", 38), ("coating", 39), ("plating", 40),
            ("materials-science", 41), ("metallurgy", 42), ("alloy", 43), ("ceramic", 44),
            ("composite", 45), ("nanomaterial", 46), ("graphene", 47), ("carbon-fiber", 48),
            ("semiconductor-material", 49), ("dielectric", 50), ("piezoelectric", 51), ("superconductor", 52),
            ("mechanical-property", 53), ("thermal-property", 54), ("electrical-property", 55), ("optical-property", 56),
            ("characterization", 57), ("microscopy", 58), ("SEM", 59), ("TEM", 60),
            ("AFM", 61), ("surface-analysis", 62), ("thin-film", 63), ("deposition", 64),
            ("CVD", 65), ("PVD", 66), ("ALD", 67), ("epitaxy", 68),
            ("chemical-engineering", 69), ("process-engineering", 70), ("reactor", 71), ("heat-exchanger", 72),
            ("distillation-column", 73), ("separation", 74), ("purification", 75), ("scale-up", 76),
            ("pilot-plant", 77), ("production", 78), ("quality-control", 79), ("GMP", 80),
            # Chinese chemistry terms
            ("化学", 81), ("有机", 82), ("无机", 83), ("分析", 84),
            ("合成", 85), ("催化", 86), ("反应", 87), ("试剂", 88),
            ("溶剂", 89), ("浓度", 90), ("色谱", 91), ("光谱", 92),
            ("质谱", 93), ("核磁共振", 94), ("X射线衍射", 95), ("蒸馏", 96),
            ("萃取", 97), ("结晶", 98), ("氧化还原", 99), ("电化学", 100),
            ("腐蚀", 101), ("涂层", 102), ("镀层", 103), ("材料科学", 104),
            ("冶金", 105), ("合金", 106), ("陶瓷", 107), ("复合材料", 108),
            ("纳米材料", 109), ("石墨烯", 110), ("碳纤维", 111), ("超导体", 112),
            ("表征", 113), ("电子显微镜", 114), ("薄膜", 115), ("沉积", 116),
            ("化学工程", 117), ("反应器", 118), ("分离", 119), ("纯化", 120),
        ],
    },
    "environment": {
        "id": "environment",
        "name": "环境 / 能源",
        "icon": "🌱",
        "description": "环境科学、可再生能源、碳中和、可持续发展等专业术语",
        "words": [
            # Environment / Energy English
            ("environment", 1), ("environmental", 2), ("ecology", 3), ("ecosystem", 4),
            ("biodiversity", 5), ("conservation", 6), ("habitat", 7), ("wetland", 8),
            ("climate-change", 9), ("global-warming", 10), ("greenhouse-gas", 11), ("CO2", 12),
            ("carbon-emission", 13), ("carbon-footprint", 14), ("carbon-neutral", 15), ("net-zero", 16),
            ("carbon-credit", 17), ("carbon-trading", 18), ("carbon-capture", 19), ("carbon-storage", 20),
            ("decarbonization", 21), ("mitigation", 22), ("adaptation", 23), ("climate-resilience", 24),
            ("Paris-Agreement", 25), ("COP", 26), ("IPCC", 27), ("NDC", 28),
            ("air-quality", 29), ("PM2.5", 30), ("PM10", 31), ("AQI", 32),
            ("water-quality", 33), ("wastewater-treatment", 34), ("desalination", 35), ("groundwater", 36),
            ("solid-waste", 37), ("hazardous-waste", 38), ("recycling", 39), ("circular-economy", 40),
            ("pollution", 41), ("contamination", 42), ("remediation", 43), ("brownfield", 44),
            ("environmental-impact", 45), ("EIA", 46), ("life-cycle-assessment", 47), ("sustainability", 48),
            ("ESG", 49), ("green-finance", 50), ("sustainable-development", 51), ("SDG", 52),
            # Energy
            ("energy", 53), ("renewable", 54), ("solar", 55), ("photovoltaic", 56),
            ("wind-power", 57), ("offshore-wind", 58), ("hydropower", 59), ("geothermal", 60),
            ("biomass", 61), ("biofuel", 62), ("hydrogen", 63), ("green-hydrogen", 64),
            ("fuel-cell", 65), ("nuclear", 66), ("fission", 67), ("fusion", 68),
            ("energy-storage", 69), ("battery-storage", 70), ("pumped-hydro", 71), ("grid", 72),
            ("smart-grid", 73), ("distributed-generation", 74), ("microgrid", 75), ("demand-response", 76),
            ("energy-efficiency", 77), ("energy-management", 78), ("power-generation", 79), ("transmission", 80),
            # Chinese environment terms
            ("环境", 81), ("生态", 82), ("生物多样性", 83), ("保护", 84),
            ("气候变化", 85), ("温室效应", 86), ("碳排放", 87), ("碳中和", 88),
            ("碳达峰", 89), ("碳交易", 90), ("碳捕集", 91), ("减排", 92),
            ("空气质量", 93), ("水质", 94), ("污水处理", 95), ("固废", 96),
            ("危废", 97), ("循环经济", 98), ("可持续发展", 99), ("绿色金融", 100),
            ("可再生能源", 101), ("太阳能", 102), ("光伏", 103), ("风电", 104),
            ("水电", 105), ("地热", 106), ("氢能", 107), ("核能", 108),
            ("储能", 109), ("锂电池", 110), ("特高压", 111), ("西电东送", 112),
            ("节能", 113), ("能源管理", 114), ("环境影响评价", 115), ("排污许可", 116),
            ("生态修复", 117), ("退耕还林", 118), ("国家公园", 119), ("双碳目标", 120),
        ],
    },
    "academic_general": {
        "id": "academic_general",
        "name": "学术通用",
        "icon": "📚",
        "description": "论文写作、研究方法、学术发表、高等教育等通用学术术语",
        "words": [
            # Academic English
            ("abstract", 1), ("introduction", 2), ("literature-review", 3), ("methodology", 4),
            ("results", 5), ("discussion", 6), ("conclusion", 7), ("acknowledgments", 8),
            ("references", 9), ("bibliography", 10), ("appendix", 11), ("supplementary", 12),
            ("hypothesis", 13), ("research-question", 14), ("thesis", 15), ("dissertation", 16),
            ("peer-review", 17), ("impact-factor", 18), ("citation-index", 19), ("h-index", 20),
            ("open-access", 21), ("preprint", 22), ("arXiv", 23), ("DOI", 24),
            ("journal", 25), ("conference-proceedings", 26), ("manuscript", 27), ("submission", 28),
            ("revision", 29), ("resubmission", 30), ("acceptance", 31), ("publication", 32),
            ("theoretical", 33), ("empirical", 34), ("qualitative", 35), ("quantitative", 36),
            ("mixed-methods", 37), ("case-study", 38), ("longitudinal", 39), ("cross-sectional", 40),
            ("experimental", 41), ("observational", 42), ("survey", 43), ("interview", 44),
            ("focus-group", 45), ("ethnography", 46), ("phenomenology", 47), ("grounded-theory", 48),
            ("sampling", 49), ("sample-size", 50), ("statistical-significance", 51), ("p-value", 52),
            ("confidence-interval", 53), ("standard-deviation", 54), ("effect-size", 55), ("correlation", 56),
            ("regression", 57), ("factor-analysis", 58), ("reliability", 59), ("validity", 60),
            ("research-ethics", 61), ("plagiarism", 62), ("authorship", 63), ("conflict-of-interest", 64),
            ("funding", 65), ("grant", 66), ("fellowship", 67), ("scholarship", 68),
            ("postdoc", 69), ("tenure", 70), ("sabbatical", 71), ("colloquium", 72),
            ("interdisciplinary", 73), ("multidisciplinary", 74), ("transdisciplinary", 75), ("cross-disciplinary", 76),
            ("pedagogy", 77), ("curriculum", 78), ("syllabus", 79), ("assessment", 80),
            ("rubric", 81), ("accreditation", 82), ("semester", 83), ("matriculation", 84),
            # Chinese academic terms
            ("摘要", 85), ("引言", 86), ("文献综述", 87), ("方法", 88),
            ("结果与讨论", 89), ("结论", 90), ("参考文献", 91), ("致谢", 92),
            ("假设", 93), ("研究问题", 94), ("论文", 95), ("学位论文", 96),
            ("同行评审", 97), ("影响因子", 98), ("引用率", 99), ("开放获取", 100),
            ("预印本", 101), ("期刊", 102), ("会议论文", 103), ("投稿", 104),
            ("修改稿", 105), ("录用", 106), ("发表", 107), ("检索", 108),
            ("定性研究", 109), ("定量研究", 110), ("实证研究", 111), ("案例研究", 112),
            ("问卷", 113), ("访谈", 114), ("样本量", 115), ("显著性", 116),
            ("相关性", 117), ("回归分析", 118), ("因子分析", 119), ("信效度", 120),
        ],
    },
}


def get_domain_weight_multiplier(domain_id: str, priority_rank: int | None = None) -> float:
    """Calculate weight multiplier for a domain based on priority rank.

    Rank 1 (highest): 3.0x
    Rank 2:          2.0x
    Rank 3:          1.5x
    Rank 4:          1.3x
    Rank 5:          1.1x
    Rank 6+:         1.0x
    No rank:         0.5x (background, lower than corpus-extracted words)
    """
    if priority_rank is None:
        return 0.5
    multipliers = {1: 3.0, 2: 2.0, 3: 1.5, 4: 1.3, 5: 1.1}
    return multipliers.get(priority_rank, 1.0)


def build_domain_lexicon(domain_priorities: list[tuple[str, int]]) -> list[tuple[str, str, int]]:
    """Build a lexicon from selected domains with priority-based weights.

    Args:
        domain_priorities: list of (domain_id, priority_rank) tuples.
                           Rank 1 = highest priority.

    Returns:
        list of (term, pinyin, weight) tuples ready for lexicon merging.
    """
    from academic_ime.pinyin_utils import term_to_pinyin

    entries: list[tuple[str, str, int]] = []
    base_weight = 1000

    for domain_id, rank in domain_priorities:
        if domain_id not in DOMAINS:
            continue
        multiplier = get_domain_weight_multiplier(domain_id, rank)
        for word, base_rank in DOMAINS[domain_id]["words"]:
            pinyin = term_to_pinyin(word)
            # Higher rank words within domain get higher base weight
            internal_weight = max(100, 500 - base_rank * 2)
            weight = int(base_weight * multiplier) + internal_weight
            entries.append((word, pinyin, weight))

    return entries


def get_domain_list() -> list[dict[str, str]]:
    """Return a lightweight list of domain metadata for the GUI."""
    return [
        {"id": d["id"], "name": d["name"], "icon": d["icon"], "description": d["description"]}
        for d in DOMAINS.values()
    ]
