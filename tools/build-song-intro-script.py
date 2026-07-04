import csv
import re
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INTRO_MD = ROOT / "output" / "song-intros-by-year-v1.md"
LOOKUP_CSV = ROOT / "output" / "song-release-years-lookup.csv"
OUT_MD = ROOT / "output" / "song-intros-by-year-release-years-v1.md"
OUT_CSV = ROOT / "output" / "song-intros-by-year-release-years-v1.csv"


MANUAL_RELEASE_YEARS = {
    ("2022", "16", "带我走 (Live)", "苏打绿"): ("2008", "manual: original song release year; QQ live page has no public date"),
    ("2023", "41", "我就不爱唱情歌 (Live)", "大张伟, 汪苏泷, 刘宇宁"): ("2022", "manual: Our Song season 3 performance year; QQ page has no public date"),
    ("2024", "2", "有没有一首歌会让你想起我 (Live)", "胡彦斌, 陆毅, 弹壳, 宝石Gem"): ("2023", "manual: Call Me by Fire season 3 performance year; QQ page has no public date"),
    ("2024", "7", "黑夜问白天 (Live)", "胡兵, 品冠, 胡彦斌, 魏巡"): ("2023", "manual: Call Me by Fire season 3 performance year; QQ page has no public date"),
    ("2024", "8", "破茧 (2023披荆斩棘的哥哥第三季现场)", "胡彦斌, 魏巡, 伯远"): ("2023", "manual: year appears in live-version title; QQ page has no public date"),
    ("2024", "12", "华山论剑：冠世一战 (Live)", "方锦龙, 郭雅志, 李延亮, 赵兆交响乐团"): ("2023", "manual: Call Me by Fire season 3 performance year; QQ page has no public date"),
    ("2024", "13", "阳光开朗大男孩 (Live)", "李昂星"): ("2021", "manual: original song publication year; QQ live page has no public date"),
    ("2024", "20", "三生三世 (2021时光音乐会第6期现场)", "林志炫"): ("2021", "manual: year appears in live-version title; QQ page has no public date"),
}


ENGLISH_OVERRIDES = {
    "旧诗": "Old Poem",
    "想念拟人化": "Missing You Personified",
    "晚安": "Goodnight",
    "会长大的幸福": "Happiness That Will Grow Up",
    "蔓延": "Spreading",
    "青春不老": "Youth Never Grows Old",
    "爱不过": "Love, But Not Enough",
    "有可能的夜晚 (Live)": "A Possible Night (Live)",
    "任我行": "Let Me Roam",
    "我是如此相信": "I Believe So Deeply",
    "有谱 (Live)": "In Tune (Live)",
    "我想要 (Live)": "I Want (Live)",
    "月亮说": "The Moon Says",
    "搜神记 (Live)": "Searching for the Divine (Live)",
    "我们的爱 (Live)": "Our Love (Live)",
    "带我走 (Live)": "Take Me Away (Live)",
    "归梦长": "Long Dream of Return",
    "葡萄成熟时 (Live)": "When the Grapes Ripen (Live)",
    "昨日青空": "Yesterday's Blue Sky",
    "不流泪的机场": "The Airport Without Tears",
    "蓝色降落伞": "Blue Parachute",
    "不惜时光": "No Regret for Time",
    "情景剧": "Scene Play",
    "最佳损友 (Live)": "Best Bad Friend (Live)",
    "我爱过你": "I Loved You",
    "光之翼 (Live)": "Wings of Light (Live)",
    "大眠": "Deep Sleep",
    "你爱我吗": "Do You Love Me",
    "藏": "Hidden",
    "姊姊妹妹站起来 (Live)": "Sisters, Stand Up (Live)",
    "拆穿": "Exposed",
    "也罢 (Live)": "So Be It (Live)",
    "偶像": "Idol",
    "忽而今夏": "Suddenly This Summer",
    "空": "Empty",
    "普通": "Ordinary",
    "一滴泪的时间 (Live)": "The Time of One Tear (Live)",
    "倾城 (Live)": "Captivating City (Live)",
    "春秋": "Spring and Autumn",
    "同花顺": "Same Suit",
    "世界上不存在的歌 (2020重唱版)": "A Song That Does Not Exist in the World (2020 Re-Sung Version)",
    "落在生命里的光 (Live)": "The Light That Fell Into Life (Live)",
    "你的眼眸是蔚蓝色海洋": "Your Eyes Are a Blue Ocean",
    "指纹": "Fingerprint",
    "喜欢": "Like",
    "我以为": "I Thought",
    "陀飞轮": "Tourbillon",
    "水手公园": "Sailor Park",
    "夜里无星": "No Stars at Night",
    "惊天动地": "Earthshaking",
    "开往早晨的午夜 (Live)": "Midnight Heading Toward Morning (Live)",
    "你要如何我们就如何 (Live)": "Whatever You Want, We Will Be (Live)",
    "千金散尽": "Spend Every Fortune",
    "不摇滚": "Not Rock",
    "满怀可爱所向披靡！ (Live)": "Armed With Cuteness, Unstoppable! (Live)",
    "再一起": "Together Again",
    "身不由己": "Beyond My Control",
    "步步": "Step by Step",
    "心门": "Heart Door",
    "美好的事可不可以发生在我身上 (Live)": "Can Something Beautiful Happen to Me (Live)",
    "让我欢喜让我忧 (Live)": "You Make Me Happy and Worried (Live)",
    "浪人情歌 (Live)": "Wanderer's Love Song (Live)",
    "是妈妈是女儿": "Mother and Daughter",
    "玩乐": "Play",
    "慢冷 (Live)": "Slow to Cool (Live)",
    "归零": "Reset to Zero",
    "月烬无声": "Moon Ashes in Silence",
    "病态": "Unwell",
    "开花的星星 (Live)": "Blooming Stars (Live)",
    "超黏人的歌 (怎么我睡不着你也不来救我/胡撸胡撸瓢儿) (Live)": "A Super Clingy Song (Live)",
    "我可以 (Live)": "I Can (Live)",
    "桃花诺": "Peach Blossom Promise",
    "嘉宾 (Live)": "Guest (Live)",
    "心要野 (Live)": "The Heart Must Be Wild (Live)",
    "山河图": "Map of Mountains and Rivers",
    "无数": "Countless",
    "毛雪汪": "Mao Xue Wang",
    "一生的风": "A Lifetime of Wind",
    "第一天 (Live)": "The First Day (Live)",
    "寂寞的恋人啊 (Live)": "Lonely Lover (Live)",
    "悬崖 (Live)": "Cliff (Live)",
    "骗": "Lie",
    "纯真 #MaydayBlue20th": "Innocence #MaydayBlue20th",
    "光的方向": "Direction of Light",
    "深情相拥 (Live)": "Deep Embrace (Live)",
    "盛夏光年": "Summer Light Years",
    "影帝 (Live)": "Best Actor (Live)",
    "瓦尔登湖": "Walden Lake",
    "我就不爱唱情歌 (Live)": "I Just Do Not Like Singing Love Songs (Live)",
    "两个人不等于我们 (Live)": "Two People Do Not Equal Us (Live)",
    "那一年 (Live)": "That Year (Live)",
    "迟到 (Live)": "Late Arrival (Live)",
    "遇到 (Live)": "Encounter (Live)",
    "悬溺": "Suspended Drowning",
    "凤凰花开的路口": "The Crossing Where Flame Trees Bloom",
    "没完": "Unfinished",
    "慢慢喜欢你 (Live at EasON AIR)": "Slowly Falling for You (Live at EasON AIR)",
    "下周同样时间 (再见) (Live)": "Same Time Next Week (Goodbye) (Live)",
    "有没有一首歌会让你想起我 (Live)": "Is There a Song That Makes You Think of Me (Live)",
    "逃亡": "Escape",
    "不必在乎我是谁 (Live)": "No Need to Care Who I Am (Live)",
    "骄傲的少年": "Proud Youth",
    "漫步人生路 (Live)": "Strolling Through Life (Live)",
    "黑夜问白天 (Live)": "Night Asks Day (Live)",
    "破茧 (2023披荆斩棘的哥哥第三季现场)": "Breaking the Cocoon (Call Me by Fire 2023 Live)",
    "岁月 (Live)": "Years (Live)",
    "自然醒": "Wake Naturally",
    "华山论剑：冠世一战 (Live)": "Huashan Sword Debate: The Ultimate Battle (Live)",
    "阳光开朗大男孩 (Live)": "Sunny Cheerful Big Boy (Live)",
    "想着你 (Live)": "Thinking of You (Live)",
    "登高 (Live)": "Climbing High (Live)",
    "一夜": "One Night",
    "青春 (Live)": "Youth (Live)",
    "光明 (Live)": "Light (Live)",
    "原来的我 (Live)": "The Original Me (Live)",
    "三生三世 (2021时光音乐会第6期现场)": "Three Lives, Three Worlds (Time Concert 2021 Live)",
    "当年情 (Live)": "Affection of Those Years (Live)",
    "小满足": "Small Satisfaction",
    "假行僧": "Fake Monk",
    "膨胀": "Inflated",
    "千面": "A Thousand Faces",
    "东海老人": "Old Man of the East Sea",
    "讲话是闭嘴的时候": "Speaking Is the Time to Be Silent",
    "同乘": "Riding Together",
    "小丑女": "Clown Girl",
    "出现又离开 (Live)": "Appear and Leave (Live)",
    "你会成为你想的那个人 (Live)": "You Will Become Who You Want to Be (Live)",
    "相思 (Live)": "Longing (Live)",
    "跟着你到天边 (Live)": "Following You to the Edge of the Sky (Live)",
    "得过且过的勇者 (Funk版)": "The Getting-By Hero (Funk Version)",
    "续写": "Continue Writing",
    "你的年纪 (Live)": "Your Age (Live)",
    "北戴河之歌": "Song of Beidaihe",
    "她等在午夜前": "She Waits Before Midnight",
    "霓裳": "Rainbow Garment",
    "你好，我是____": "Hello, I Am ____",
    "五光十色": "Dazzling Colors",
    "静止 (Live)": "Still (Live)",
    "将进酒 (Live)": "Bring in the Wine (Live)",
    "麒麟": "Qilin",
    "再见萤火虫 (Live)": "Goodbye, Firefly (Live)",
    "少年狂想录": "Youth Rhapsody",
    "走吧，我没想过这是最后的家 (Hello,Bye)": "Let's Go, I Never Thought This Was the Last Home (Hello,Bye)",
    "唯爱": "Only Love",
    "我爱你，再见 (Live)": "I Love You, Goodbye (Live)",
    "江湖写照 (Single Version)": "Portrait of the Martial World (Single Version)",
    "行走的鱼 (Live)": "Walking Fish (Live)",
    "只有风知道 (Live)": "Only the Wind Knows (Live)",
    "热烈的少年 (Live)": "Passionate Youth (Live)",
    "我执剑主锋芒": "I Hold the Sword and Lead the Edge",
    "如果有来生 (Live)": "If There Is a Next Life (Live)",
    "赴狂澜": "Into the Wild Waves",
    "炽火同行": "Walking Together Through Blazing Fire",
    "薄荷夏天 (Live)": "Mint Summer (Live)",
    "无人的海边 (Live)": "Empty Seaside (Live)",
    "梦臆 (Live)": "Dream Delusion (Live)",
    "雨 (Live)": "Rain (Live)",
    "字字句句 (Live)": "Every Word, Every Sentence (Live)",
    "好不容易": "Not Easy",
    "孤星": "Lonely Star",
    "少年西西弗斯": "Young Sisyphus",
    "流花 (Love Herby)": "Flowing Flowers (Love Herby)",
    "拭剑": "Wiping the Sword",
    "说侠": "Speaking of Heroes",
    "心途（Fly）": "Heart Road (Fly)",
    "我想念 (Live)": "I Miss You (Live)",
    "这条小鱼在乎 (I'm a little fish)": "This Little Fish Cares (I'm a Little Fish)",
    "奔": "Run",
    "修炼爱情 (Live)": "Practice Love (Live)",
    "相爱后动物感伤 (Live)": "Animals Feel Sad After Love (Live)",
    "咕叽咕叽 (Live)": "Gu Ji Gu Ji (Live)",
    "不痛 (Live)": "No Pain (Live)",
    "茧蜜 (有歌第二季第2期) (Live)": "Cocoon Honey (Live)",
    "爱晚亭边": "Beside Aiwan Pavilion",
    "借过一下 (Live)": "Excuse Me, Passing Through (Live)",
    "一样的月光": "The Same Moonlight",
    "感官先生 (Live)": "Mr. Senses (Live)",
    "苍苍": "Vast and Grey",
    "星夜": "Starry Night",
    "天气恋人": "Weather Lover",
    "女孩，女孩！": "Girl, Girl!",
    "净含量750毫升": "Net Content: 750 ml",
    "莉莉安 (Live)": "Lillian (Live)",
    "成吉思汗 (Live)": "Genghis Khan (Live)",
    "阳光下": "Under the Sun",
    "从简": "Keep It Simple",
    "是的我们跳着舞": "Yes, We Are Dancing",
    "纸船": "Paper Boat",
    "泪是爱的自证书": "Tears Are Love's Own Certificate",
    "美力场": "Field of Beauty",
    "轮廓": "Outline",
    "篇章 (开启新篇)": "Chapter (Opening a New Chapter)",
    "黑与白": "Black and White",
    "戒伞": "Putting Away the Umbrella",
    "怜悯 姜蔓": "Mercy: Jiang Man",
    "平庸 (Live)": "Ordinary (Live)",
    "讯号 (Live)": "Signal (Live)",
    "还我": "Give It Back to Me",
    "你": "You",
    "浪费 (Live)": "Waste (Live)",
    "不爱我就拉倒": "If You Do Not Love Me, Fine",
    "日落计数器": "Sunset Counter",
    "谢礼 (Thank-You Gift)": "Thank-You Gift",
    "要不要投降": "Should I Surrender",
    "初识": "First Encounter",
    "怜悯 (Live)": "Mercy (Live)",
    "哑谜 (Live)": "Riddle (Live)",
    "刚好 (摇滚版)": "Just Right (Rock Version)",
    "星光": "Starlight",
    "大人 (Live)": "Grown-Up (Live)",
    "师傅，什么是爱情": "Master, What Is Love?",
    "留白 (Forgotten)": "Blank Space (Forgotten)",
    "足够 (Live)": "Enough (Live)",
}


ARTIST_OVERRIDES = {
    "亦然": "Yiran",
    "孟慧圆": "Meng Huiyuan",
    "丢火车乐队": "Lost Train Band",
    "许美静": "Mavis Hee",
    "丁一滕": "Ding Yiteng",
    "汪晨蕊": "Wang Chenrui",
    "周深": "Zhou Shen",
    "陈奕迅": "Eason Chan",
    "周杰伦": "Jay Chou",
    "李昂星": "Li Angxing",
    "杨宗纬": "Aska Yang",
    "王菀之": "Ivana Wong",
    "林俊杰": "JJ Lin",
    "苏打绿": "Sodagreen",
    "李玉刚, 剑网3": "Li Yugang, JX3",
    "杨千嬅, 刘惜君": "Miriam Yeung, Liu Xijun",
    "尤长靖": "You Zhangjing",
    "张靓颖": "Jane Zhang",
    "陈粒": "Chen Li",
    "毛不易, 李克勤": "Mao Buyi, Hacken Lee",
    "Eric周兴哲": "Eric Chou",
    "张韶涵, 檀健次": "Angela Chang, Tan Jianci",
    "王心凌": "Cyndi Wang",
    "范逸臣 Van Fan": "Van Fan",
    "王靖雯, 唐汉霄": "Wang Jingwen, Tang Hanxiao",
    "吴莫愁, 唐汉霄, 梁龙, 苏见信 (信)": "Momo Wu, Tang Hanxiao, Liang Long, Shin",
    "小霞": "Xiao Xia",
    "刘佳琪": "Liu Jiaqi",
    "金玟岐": "Vanessa Jin",
    "汪苏泷": "Silence Wang",
    "林志炫": "Terry Lin",
    "赵紫骅": "Zhao Zihua",
    "张敬轩": "Hins Cheung",
    "林倛玉": "Lin Qiyu",
    "赵磊, 戴燕妮": "Zhao Lei, Dai Yanni",
    "杜宣达": "Du Xuanda",
    "GALA": "GALA",
    "告五人": "Accusefive",
    "胡彦斌, 告五人": "Hu Yanbin, Accusefive",
    "胡彦斌, 张钰琪": "Hu Yanbin, Zhang Yuqi",
    "八三夭乐团, 告五人": "831, Accusefive",
    "吕方, 大张伟, 翟潇闻, 汪苏泷": "David Lui, Wowkie Zhang, Zhai Xiaowen, Silence Wang",
    "余佳运": "Yu Jiayun",
    "丁当": "Della Ding",
    "五月天": "Mayday",
    "华晨宇": "Hua Chenyu",
    "杨宗纬, 毕雯珺": "Aska Yang, Bi Wenjun",
    "杨宗纬, 于文文": "Aska Yang, Kelly Yu",
    "黄绮珊, 希林娜依高": "Huang Qishan, Curley G",
    "方大同": "Khalil Fong",
    "张碧晨, 希林娜依高": "Zhang Bichen, Curley G",
    "耿斯汉": "Geng Sihan",
    "薛之谦": "Joker Xue",
    "大张伟, 焦迈奇": "Wowkie Zhang, Jiao Maiqi",
    "蔡旻佑": "Evan Yo",
    "G.E.M. 邓紫棋": "G.E.M.",
    "Faye 詹雯婷, 张远": "Faye, Zhang Yuan",
    "后海大鲨鱼": "Queen Sea Big Shark",
    "凤凰传奇": "Phoenix Legend",
    "毛不易, 李雪琴": "Mao Buyi, Li Xueqin",
    "那英": "Na Ying",
    "杨宗纬, 张韶涵, 陈立农": "Aska Yang, Angela Chang, Chen Linong",
    "魏如萱": "Waa Wei",
    "张信哲, 那英": "Jeff Chang, Na Ying",
    "五月天 阿信": "Ashin",
    "周笔畅, 单依纯": "Bibi Zhou, Shan Yichun",
    "周云蓬": "Zhou Yunpeng",
    "大张伟, 汪苏泷, 刘宇宁": "Wowkie Zhang, Silence Wang, Liu Yuning",
    "张碧晨, Eric周兴哲": "Zhang Bichen, Eric Chou",
    "大张伟, 汪苏泷": "Wowkie Zhang, Silence Wang",
    "艾薇 Ivy, 周菲戈": "Ivy Lee, Zhou Feige",
    "陈卓璇": "Chen Zhuoxuan",
    "葛东琪": "Ge Dongqi",
    "林志炫": "Terry Lin",
    "陈楚生": "Chen Chusheng",
    "胡彦斌, 陆毅, 弹壳, 宝石Gem": "Hu Yanbin, Lu Yi, Danko, Gem",
    "孙燕姿": "Stefanie Sun",
    "苏见信 (信), 胡彦斌": "Shin, Hu Yanbin",
    "南征北战NZBZ": "NZBZ",
    "裁缝铺, 邢晗铭, 中国潮音": "Tailor Shop, Xing Hanming, China Chic",
    "胡兵, 品冠, 胡彦斌, 魏巡": "Hu Bing, Victor Wong, Hu Yanbin, Wei Xun",
    "胡彦斌, 魏巡, 伯远": "Hu Yanbin, Wei Xun, Boyuan",
    "黄绮珊, 周深": "Huang Qishan, Zhou Shen",
    "方锦龙, 郭雅志, 李延亮, 赵兆交响乐团": "Fang Jinlong, Guo Yazhi, Li Yanliang, Zhao Zhao Symphony Orchestra",
    "毛不易, 裁缝铺, 中国潮音": "Mao Buyi, Tailor Shop, China Chic",
    "大张伟, 裁缝铺, 中国潮音": "Wowkie Zhang, Tailor Shop, China Chic",
    "陆毅, 胡彦斌, 唐禹哲, 弹壳": "Lu Yi, Hu Yanbin, Danson Tang, Danko",
    "陈楚生, 八三夭阿璞": "Chen Chusheng, A-Pu",
    "古巨基, 陈楚生": "Leo Ku, Chen Chusheng",
    "杨宗纬, 刘惜君": "Aska Yang, Liu Xijun",
    "于贞, 阿达娃, 沙一汀EL, 孙瑄阳Xtina": "Yu Zhen, Adawa, Sha Yiting EL, Sun Xuanyang Xtina",
    "陆通": "Lu Tong",
    "裁缝铺": "Tailor Shop",
    "易烊千玺": "Jackson Yee",
    "杨和苏KeyNG": "KeyNG",
    "梁博": "Liang Bo",
    "胡彦斌, 毛阿敏": "Hu Yanbin, Mao Amin",
    "三无Marblue": "Sanwu Marblue",
    "剑网3, JX3暗箱组合": "JX3, JX3 Anxiang Group",
    "单依纯": "Shan Yichun",
    "凡清 (Fanish)": "Fanish",
    "大张伟, 杨乃文": "Wowkie Zhang, Faith Yang",
    "陈楚生, 蔡国庆, 李玖哲, 宝石Gem": "Chen Chusheng, Cai Guoqing, Nicky Lee, Gem",
    "早安": "Good Morning",
    "苏诗丁": "Juno Su",
    "剑网3, 五音Jw, 陆深": "JX3, Wuyin Jw, Lu Shen",
    "简单对话 A Little Conversation": "A Little Conversation",
    "Faye 詹雯婷": "Faye",
    "大张伟, 毛不易": "Wowkie Zhang, Mao Buyi",
    "汪苏泷": "Silence Wang",
    "霓虹花园NeonGarden": "NeonGarden",
    "黄誉博, 赖美云, 张星特": "Huang Yubo, Lai Meiyun, Zhang Xingte",
    "谭维维": "Tan Weiwei",
    "剑网3, Assen捷, 司夏, Smile_小千": "JX3, Assen Jie, Sixia, Smile Xiao Qian",
    "曹杨": "Cao Yang",
    "姚晓棠": "Yao Xiaotang",
    "张碧晨, 霓虹花园NeonGarden": "Zhang Bichen, NeonGarden",
    "李承铉, 希林娜依高": "Nathan Lee, Curley G",
    "陈冰, 艾热AIR": "Chen Bing, AIR",
    "张碧晨, 王赫野": "Zhang Bichen, Wang Heye",
    "钟凯琳": "Zhong Kailin",
    "孙天宇": "Sun Tianyu",
    "朴树": "Pu Shu",
    "袁娅维TIA RAY": "TIA RAY",
    "剑网3, 五音Jw, Smile_小千, 柒落Seven": "JX3, Wuyin Jw, Smile Xiao Qian, Seven",
    "老虎欧巴": "Tiger Oppa",
    "崔迪": "Cui Di",
    "汪苏泷, 王赫野": "Silence Wang, Wang Heye",
    "王OK, 洪佩瑜": "Wang OK, Pei-Yu Hung",
    "窦靖童": "Leah Dou",
    "徐佳莹": "LaLa Hsu",
    "张碧晨, 高睿": "Zhang Bichen, Gao Rui",
    "小时姑娘": "Xiaoshi Guniang",
    "胡彦斌, Jony J": "Hu Yanbin, Jony J",
    "希林娜依高": "Curley G",
    "杨润泽": "Yang Runze",
    "陈雪燃": "Chen Xueran",
    "金玟岐": "Vanessa Jin",
    "姚晓棠, 张郁梓": "Yao Xiaotang, Zhang Yuzi",
    "呼和图拉嘎": "Huhe Tulaga",
    "满江": "Man Jiang",
    "孟慧圆": "Meng Huiyuan",
    "张靓颖, 毛不易": "Jane Zhang, Mao Buyi",
    "薛之谦, 郁可唯": "Joker Xue, Yisa Yu",
    "陈婧霏": "Chen Jingfei",
    "赵紫骅": "Zhao Zihua",
    "王赫野": "Wang Heye",
    "苏诗丁": "Juno Su",
    "琥珀xisa": "Amber Xisa",
    "张碧晨": "Zhang Bichen",
    "S.H.E": "S.H.E",
    "田馥甄": "Hebe Tien",
    "莫非定律乐团": "MFLD",
    "银河快递 (Galaxy Express)": "Galaxy Express",
    "王梓赫Ray": "Ray Wang",
    "李楚然": "Li Churan",
    "Eric周兴哲, 林宥嘉, 汪苏泷": "Eric Chou, Yoga Lin, Silence Wang",
    "张栋梁, 银河快递 (Galaxy Express)": "Nicholas Teo, Galaxy Express",
}


def has_cjk(value):
    return bool(re.search(r"[\u3400-\u9fff]", value or ""))


def english_title(title):
    if title in ENGLISH_OVERRIDES:
        return ENGLISH_OVERRIDES[title]
    return title


def english_artist(artist):
    if artist in ARTIST_OVERRIDES:
        return ARTIST_OVERRIDES[artist]
    return artist


def load_release_lookup():
    lookup = {}
    with LOOKUP_CSV.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            manual = MANUAL_RELEASE_YEARS.get((row["Year"], row["Rank"], row["Song"], row["Artist"]))
            if manual:
                row["ReleaseYear"], row["LookupStatus"] = manual
            lookup[(row["Year"], row["Rank"], row["Song"], row["Artist"])] = row
    return lookup


def parse_intro_file():
    lines = INTRO_MD.read_text(encoding="utf-8").splitlines()
    records = []
    current = None
    for line in lines:
        match = re.match(r"^### (\d{4})\.(\d{2}) - (.*?) - (.*)$", line)
        if match:
            if current:
                records.append(current)
            year, rank, song, artist = match.groups()
            current = {
                "Year": year,
                "Rank": str(int(rank)),
                "Song": song,
                "Artist": artist,
                "IntroLines": [],
            }
        elif current is not None:
            if line.startswith("## "):
                continue
            if line.strip():
                current["IntroLines"].append(line)
    if current:
        records.append(current)
    return records


def main():
    lookup = load_release_lookup()
    records = parse_intro_file()
    out_lines = [
        "# Song Intros by Year with Release Years - v1",
        "",
        "Structure for each song:",
        "",
        "1. 4-6 line English intro",
        "2. Optional English display title line for Chinese-title songs by Chinese-language artists",
        "3. Release year",
        "",
        "Release years come from QQ Music structured song detail pages where available. A small number of live/program tracks without QQ public dates use manual fallback years noted in the CSV.",
    ]
    csv_rows = []
    current_year = None
    for record in records:
        if record["Year"] != current_year:
            current_year = record["Year"]
            out_lines.extend(["", f"## {current_year}"])
        lookup_row = lookup.get((record["Year"], record["Rank"], record["Song"], record["Artist"]), {})
        release_year = lookup_row.get("ReleaseYear", "")
        if not release_year:
            release_year = "Unknown"
        display_needed = has_cjk(record["Song"]) and has_cjk(record["Artist"])
        display = ""
        if display_needed:
            display = f"{english_title(record['Song'])} - {english_artist(record['Artist'])}"
        out_lines.extend(["", f"### {record['Year']}.{int(record['Rank']):02d} - {record['Song']} - {record['Artist']}"])
        out_lines.extend(record["IntroLines"][:6])
        if display:
            out_lines.extend(["", display])
        out_lines.extend(["", f"Release year: {release_year}"])
        csv_rows.append(
            {
                "Year": record["Year"],
                "Rank": record["Rank"],
                "Song": record["Song"],
                "Artist": record["Artist"],
                "EnglishDisplayLine": display,
                "ReleaseYear": release_year,
                "ReleaseDate": lookup_row.get("ReleaseDate", ""),
                "ReleaseYearSource": lookup_row.get("LookupStatus", ""),
                "QQSongURL": lookup_row.get("QQSongURL", ""),
                "Intro": "\n".join(record["IntroLines"][:6]),
            }
        )
    OUT_MD.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_CSV}")
    print(f"records: {len(csv_rows)}")
    missing = [r for r in csv_rows if r["ReleaseYear"] == "Unknown"]
    print(f"unknown release years: {len(missing)}")
    missing_display = [r for r in csv_rows if has_cjk(r["Song"]) and has_cjk(r["Artist"]) and not r["EnglishDisplayLine"]]
    print(f"missing English display lines: {len(missing_display)}")


if __name__ == "__main__":
    main()
