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
