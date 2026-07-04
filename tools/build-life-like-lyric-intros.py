import csv
import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v10-varied-openings.csv"
OUT_MD = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v12-life-like-relatable.md"
OUT_CSV = ROOT / "output" / "song-intros-by-year-same-singer-moved-back-v12-life-like-relatable.csv"


OBSOLETE_INTRO_FIELDS = {
    "ChineseIntroLyricMeaning",
    "EnglishIntroLyricMeaning",
}


THEME_CN = {
    "love": "想靠近一个人，却又怕打扰",
    "heartbreak": "明明已经过去，心里还是会被轻轻碰一下",
    "memory": "某个普通物件突然把回忆带回来",
    "healing": "日子没有马上变好，但人开始慢慢能呼吸",
    "growth": "把委屈咽下去之后，还是试着往前走",
    "city-night": "夜深以后，那些白天没空想的事又冒出来",
    "energy": "忍了很久的情绪终于想冲出去",
    "personal": "很多话没有说给别人听，只是在心里过了一遍",
}


THEME_EN = {
    "love": "wanting to move closer while still afraid of asking too much",
    "heartbreak": "something that has passed still touching the heart without warning",
    "memory": "an ordinary object suddenly bringing a memory back",
    "healing": "life not becoming better at once, but breathing getting easier",
    "growth": "swallowing the hurt and still trying to move forward",
    "city-night": "the thoughts that return after the day finally goes quiet",
    "energy": "a feeling held back too long finally needing to move",
    "personal": "words that are never sent, only replayed inside",
}


MOOD_CN = {
    "melancholic": "它不把难过说得很大，只像生活里忽然安静下来的几秒。",
    "healing": "它像有人把椅子拉近一点，让你可以先坐下来。",
    "energetic": "它像把窗打开，终于让憋住的那口气出去。",
    "reflective": "它像走到路口时回头看了一眼，才发现自己已经走了很远。",
    "nostalgic": "它像翻到一张旧照片，明明没准备好，心却先软了。",
    "aspirational": "它像早上出门前的那一点亮光，提醒人还可以继续。",
}


MOOD_EN = {
    "melancholic": "It does not make sadness huge; it stays close to a few quiet seconds in daily life.",
    "healing": "It feels like someone pulling a chair closer so you can sit down first.",
    "energetic": "It feels like opening a window and letting a held breath out.",
    "reflective": "It is like glancing back at a crossing and realizing how far you have walked.",
    "nostalgic": "It feels like finding an old photo before the heart is ready for it.",
    "aspirational": "It carries the small light of leaving home in the morning and trying again.",
}


ENERGY_CN = {
    "low": "所以它适合轻轻带进来，像把声音放低一点。",
    "medium": "所以它不用催促，只要让情绪一步一步走出来。",
    "high": "所以它可以直接一点，把那股压住的劲推到台前。",
}


ENERGY_EN = {
    "low": "So it should enter gently, as if the volume has been lowered.",
    "medium": "So it does not need to rush; the feeling can walk out step by step.",
    "high": "So it can arrive more directly, pushing that held-back force forward.",
}

MOOD_CN_VARIANTS = {
    "melancholic": [
        "它不把难过说得很大，只像生活里忽然安静下来的几秒。",
        "它更像某天突然没了力气，却还要把日子照常过完。",
        "它把难过放得很近，近到像一句没发出去的消息。",
        "它没有哭得很响，只是让人想起那些自己消化的晚上。",
        "它像人群散开以后，心里还留着一点没走掉的酸。",
    ],
    "healing": [
        "它像有人把椅子拉近一点，让你可以先坐下来。",
        "它没有急着安慰，只是让紧绷的人慢慢松一口气。",
        "它像一杯温水放在手边，不催你马上好起来。",
        "它让人觉得，今天撑过去一点点，也已经算数。",
        "它把情绪接住，不问你为什么还没完全放下。",
    ],
    "energetic": [
        "它像把窗打开，终于让憋住的那口气出去。",
        "它把压在胸口的劲往外推，让人想站起来。",
        "它不是轻轻带过，而是把忍了很久的话推到台前。",
        "它像走到街口忽然加快脚步，身体先替心做了决定。",
        "它让那股不想认输的劲，变得更直接一点。",
    ],
    "reflective": [
        "它像走到路口时回头看了一眼，才发现自己已经走了很远。",
        "它让人想起某个改变自己的瞬间，当时并没有察觉。",
        "它不是回到过去，而是终于看懂了当时的自己。",
        "它像整理旧东西时停了一下，才发现有些事已经变轻。",
        "它把时间放慢一点，让人听见心里真正想说的话。",
    ],
    "nostalgic": [
        "它像翻到一张旧照片，明明没准备好，心却先软了。",
        "它把回忆带回来时，不是轰轰烈烈，只是很轻地碰一下。",
        "它像某个熟悉的味道突然出现，人一下子回到从前。",
        "它让过去不是故事，而是此刻还能感觉到的温度。",
        "它像多年后再路过同一条街，才发现自己还记得细节。",
    ],
    "aspirational": [
        "它像早上出门前的那一点亮光，提醒人还可以继续。",
        "它把人从低头的状态里拉起来一点，哪怕只是一点。",
        "它像把包背上重新出门，心里还有想完成的事。",
        "它不喊口号，只让人觉得明天还值得试一次。",
        "它给人的力量很日常，像把今天重新收拾好。",
    ],
}

MOOD_EN_VARIANTS = {
    "melancholic": [
        "It does not make sadness huge; it stays close to a few quiet seconds in daily life.",
        "It feels like running out of strength for a moment and still finishing the day.",
        "It keeps sadness close, like a message that never gets sent.",
        "It does not cry loudly; it remembers the nights people handle on their own.",
        "It feels like the crowd has gone, but a small ache has stayed behind.",
    ],
    "healing": [
        "It feels like someone pulling a chair closer so you can sit down first.",
        "It does not rush to comfort anyone; it simply lets the body loosen a little.",
        "It feels like warm water set beside you, without asking you to be fine right away.",
        "It says that getting through today, even barely, still counts.",
        "It holds the feeling without asking why it has not fully passed.",
    ],
    "energetic": [
        "It feels like opening a window and letting a held breath out.",
        "It pushes the pressure in the chest outward until standing up feels natural.",
        "It does not brush the feeling aside; it brings the unsaid words forward.",
        "It feels like speeding up at a street corner before the mind has decided.",
        "It makes the refusal to give up feel more direct.",
    ],
    "reflective": [
        "It is like glancing back at a crossing and realizing how far you have walked.",
        "It recalls the moment that changed someone before they knew it was happening.",
        "It is not returning to the past; it is finally understanding who you were then.",
        "It feels like pausing while sorting old things and realizing some weight has lifted.",
        "It slows time down enough for the heart to say what it means.",
    ],
    "nostalgic": [
        "It feels like finding an old photo before the heart is ready for it.",
        "It brings memory back quietly, with just one light touch.",
        "It feels like a familiar smell returning and placing someone back in another year.",
        "It makes the past feel less like a story and more like a temperature still present.",
        "It feels like passing the same street years later and still remembering the details.",
    ],
    "aspirational": [
        "It carries the small light of leaving home in the morning and trying again.",
        "It lifts someone a little from looking down, even if only a little.",
        "It feels like putting the bag back on and stepping out with something unfinished.",
        "It does not shout; it simply makes tomorrow feel worth another try.",
        "It gives a daily kind of strength, like putting today back in order.",
    ],
}

ENERGY_CN_VARIANTS = {
    "low": [
        "所以它适合轻轻带进来，像把声音放低一点。",
        "所以开场不用太满，让那点心事慢慢靠近就好。",
        "所以它更适合留一点空白，让观众自己想起自己的事。",
        "所以声音可以先放轻，像怕惊动一个刚浮上来的念头。",
    ],
    "medium": [
        "所以它不用催促，只要让情绪一步一步走出来。",
        "所以节奏可以稳一点，让每个人慢慢跟上自己的心情。",
        "所以它适合从日常里推开，让情绪自然走到台前。",
        "所以不必急着煽动，等那份共鸣自己落下来。",
    ],
    "high": [
        "所以它可以直接一点，把那股压住的劲推到台前。",
        "所以开场可以更有力量，让积攒的情绪一下站出来。",
        "所以它不需要绕太远，可以把现场的气口直接打开。",
        "所以让它带着一点冲劲来，把心里那句没说完的话喊亮。",
    ],
}

ENERGY_EN_VARIANTS = {
    "low": [
        "So it should enter gently, as if the volume has been lowered.",
        "So the opening can stay soft and let the feeling move closer slowly.",
        "So it can leave some space for listeners to remember their own moments.",
        "So the voice can begin lightly, careful not to disturb the thought rising up.",
    ],
    "medium": [
        "So it does not need to rush; the feeling can walk out step by step.",
        "So the rhythm can stay steady while everyone catches up with their own mood.",
        "So it can open from daily life and let the emotion arrive naturally.",
        "So there is no need to push; the connection can settle on its own.",
    ],
    "high": [
        "So it can arrive more directly, pushing that held-back force forward.",
        "So the opening can carry more strength and let the stored-up feeling stand up.",
        "So it does not need a long path; it can open the room right away.",
        "So it can come in with momentum and brighten the words left unsaid.",
    ],
}

CN_CORE_PATTERNS = [
    "你可能也有过这种时候：真正留下来的不是大道理，而是{core}。",
    "它说的不是很远的故事，更像我们都遇到过的{core}。",
    "这一句情绪很生活：不是非要有答案，只是{core}。",
    "很多人会在这里想到自己，因为那里面有{core}。",
    "它把人的心事讲得很近，近到只剩下{core}。",
    "有些感受说出来会显得普通，但真的经历过，就知道那是{core}。",
]

EN_CORE_PATTERNS = [
    "You may know this kind of moment: what stays is not a big lesson, but {core}.",
    "It does not feel like a faraway story; it feels like {core}.",
    "The emotion is very close to daily life: no clear answer, just {core}.",
    "Many listeners can find themselves here, because it carries {core}.",
    "It brings the feeling close enough to become {core}.",
    "Some feelings sound simple until they have been lived; this one carries {core}.",
]

CN_LINE_DETAILS = [
    "半夜回消息前的停顿",
    "下班路上突然慢下来的脚步",
    "电梯门合上前的那一秒",
    "雨停以后还发亮的路面",
    "睡前没发出去的那行字",
    "早餐店刚冒起的热气",
    "出租车后座短暂的安静",
    "便利店灯光下的一口热饮",
    "手机屏幕暗下去后的沉默",
    "厨房小灯旁边的深呼吸",
    "公交站人群散开后的空位",
    "旧衣服口袋里摸到的纸片",
    "房间慢慢安静下来的时候",
    "车窗上往下滑的雨水",
    "桌角被风吹起的便签",
    "楼道灯亮起又暗下去的瞬间",
    "排队时被攥皱的小票",
    "枕边那本没读完的书",
    "钥匙落进碗里的轻响",
    "站台广播重复的一句话",
    "外卖袋还剩一点热气的时候",
    "洗衣机转到最后几分钟",
    "衣架上还带着冷气的外套",
    "红灯前忽然走神的片刻",
    "未接来电躺在屏幕上的安静",
    "夜里镜子上还没散开的水汽",
    "书桌上一张旧票根",
    "回家路上一盏盏退后的路灯",
    "自动贩卖机掉下一罐冰水的声音",
    "门口鞋子还没摆正的角度",
]

EN_LINE_DETAILS = [
    "the pause before replying late at night",
    "the slowed step on the way home after work",
    "the second before elevator doors close",
    "the pavement still shining after rain",
    "the sentence left unsent before sleep",
    "steam rising from a breakfast shop",
    "the brief quiet in the back seat of a taxi",
    "a warm drink under convenience-store lights",
    "the silence after a phone screen goes dark",
    "a deep breath beside a small kitchen light",
    "the empty space after people leave the bus stop",
    "a folded paper found in an old pocket",
    "the room slowly settling after the door closes",
    "rain sliding down a car window",
    "a sticky note lifting at the corner of a desk",
    "the hallway light fading after it turns on",
    "a receipt crumpled while waiting in line",
    "an unfinished book left near the pillow",
    "the small sound of keys dropping into a bowl",
    "one repeated platform announcement",
    "a delivery bag still holding a little warmth",
    "the last minutes of a washing-machine cycle",
    "a coat still carrying the cold from outside",
    "drifting off while waiting at a red light",
    "a missed call resting quietly on the screen",
    "steam still on the mirror after midnight",
    "an old ticket stub on the desk",
    "streetlights falling back one by one on the way home",
    "a cold can dropping from a vending machine",
    "shoes by the door still angled from coming home",
]


TITLE_CN_HINTS = [
    (("想念", "思念"), "像刷到一个熟悉头像时，手指停了一下。"),
    (("晚安",), "像睡前最后看一眼手机，却没有再发消息。"),
    (("我想要",), "像终于承认自己不是无所谓，而是真的想被回应。"),
    (("爱", "喜欢"), "像把聊天框打开又关上，心里还是放不下。"),
    (("再见", "离开", "逃亡"), "像走出门以后，还会下意识回头看一眼。"),
    (("光", "星", "月"), "像夜里路灯还亮着，给人一点继续走的理由。"),
    (("梦",), "像醒来以后还记得一点画面，却说不清为什么难过。"),
    (("青春", "少年"), "像很久以后想起自己曾经那么用力地相信过。"),
    (("普通", "平庸"), "像平凡的一天里，也藏着不想被看轻的心事。"),
    (("浪费",), "像明知道没有结果，却还是舍不得否定那段认真。"),
    (("雨",), "像下雨天站在屋檐下，突然什么都不想解释。"),
    (("夜",), "像灯关掉以后，白天压住的话终于浮上来。"),
]


TITLE_EN_HINTS = [
    (("missing", "miss", "想念"), "It feels like pausing on a familiar profile picture and not knowing what to do next."),
    (("goodnight", "晚安"), "It feels like checking the phone one last time before sleep and choosing not to send anything."),
    (("want", "我想要"), "It feels like finally admitting this was never indifference; it was wanting an answer."),
    (("love", "喜欢", "爱"), "It feels like opening the chat box, closing it, and still not being able to let go."),
    (("goodbye", "leave", "离开", "再见"), "It feels like walking out the door and still turning back once."),
    (("light", "moon", "star", "光", "月", "星"), "It feels like a streetlamp staying on just long enough to keep someone walking."),
    (("dream", "梦"), "It feels like waking with a piece of a dream still in the chest."),
    (("youth", "少年", "青春"), "It feels like remembering how hard you once believed in something."),
    (("ordinary", "平庸", "普通"), "It feels like an ordinary day carrying a feeling that refuses to be small."),
    (("waste", "浪费"), "It feels like knowing something failed and still refusing to call the care meaningless."),
    (("rain", "雨"), "It feels like standing under an awning and suddenly not wanting to explain anything."),
    (("night", "夜"), "It feels like the words held down all day rising after the lights go out."),
]


CN_SCENES = [
    "地铁门快关上的时候",
    "深夜便利店的灯还亮着",
    "手机屏幕暗下去又被点亮",
    "下班路上的风从袖口钻进来",
    "电梯数字一层一层往上跳",
    "厨房里只剩一盏小灯",
    "雨伞靠在门边还没收好",
    "洗衣机转到最后几分钟",
    "公交站牌下的人慢慢少了",
    "外卖袋放在桌上还冒着一点热气",
    "聊天框里的字删了又写",
    "耳机线缠在口袋里",
    "窗帘没有完全拉上",
    "杯子里的水已经凉了",
    "凌晨的街道只剩轮胎声",
    "楼道灯亮了一下又暗下去",
    "鞋柜旁边还有没拆的快递",
    "书桌上压着一张旧票根",
    "房间里只有空调很轻的声音",
    "等红灯的时候忽然走神",
    "商场快打烊时音乐还在播",
    "回家路上路灯一盏一盏退后",
    "床边的充电线绕成一团",
    "早餐摊刚收起最后一只锅",
    "雨水顺着车窗往下滑",
    "门口的鞋还保持着刚进家的角度",
    "冰箱启动的声音忽然变清楚",
    "未接来电安静地躺在屏幕上",
    "旧衣服口袋里摸到一张纸",
    "楼下有人关门，声音传得很远",
    "夜里洗手台的镜子有一点雾",
    "车厢里有人把音量调低",
    "桌角的便签被风吹起来",
    "窗外的广告牌换了颜色",
    "排队时手里攥着一张小票",
    "雨停以后地面还在反光",
    "枕头旁边还放着没读完的书",
    "自动贩卖机吐出一罐冰水",
    "楼下早餐店开始蒸出白雾",
    "深夜消息提示音响了一下",
    "衣架上的外套还带着外面的冷气",
    "出租车后座安静得有点空",
    "房门关上以后，屋里慢慢静下来",
    "手表震了一下，却不是等的人",
    "灯光照在没收拾的桌面上",
    "洗完澡的水汽还没有散",
    "站台广播重复着同一句话",
    "纸巾被攥得有点皱",
    "钥匙放进碗里发出很轻的一声",
    "窗外有人骑车经过水洼",
]


CN_OPENING_ENDINGS = [
    "那种感觉会突然靠得很近。",
    "有些心事会在这时候自己冒出来。",
    "人很容易在这一秒想起某个没说完的念头。",
    "很多话不用说出口，也会被自己听见。",
    "情绪好像没有预告，就坐到了身边。",
    "那一点说不清的反应，会忽然变得很具体。",
    "有时候，人就是在这种小地方被击中。",
    "生活很安静，心里却像被轻轻推了一下。",
    "这不是大起大落，却很容易让人代入。",
    "某个已经放下的念头，会在这里又亮一下。",
    "你可能也有过这种瞬间：什么都没发生，心却动了一下。",
    "它像把一个普通片刻，轻轻推到心口。",
]


EN_SCENES = [
    "when the subway doors are about to close",
    "under the light of a late-night convenience store",
    "when the phone screen goes dark and lights up again",
    "on the walk home after work, with wind at the cuffs",
    "as the elevator numbers climb one floor at a time",
    "with only one small kitchen light left on",
    "with the umbrella still leaning by the door",
    "during the last few minutes of the washing machine cycle",
    "under a bus stop sign as the crowd thins out",
    "beside a delivery bag still holding a little warmth",
    "inside a chat box typed, erased, and typed again",
    "with earphones tangled in a pocket",
    "beside curtains not fully closed",
    "next to a glass of water that has gone cold",
    "on a street where only tires are still making sound",
    "as the hallway light switches on and fades again",
    "beside an unopened package by the shoe cabinet",
    "over an old ticket stub on the desk",
    "in a room where only the air conditioner is audible",
    "while waiting at a red light and drifting away",
    "as music keeps playing in a mall about to close",
    "with streetlights falling back one by one on the way home",
    "beside a charging cable knotted near the bed",
    "after the breakfast stall has packed away the last pan",
    "as rain slides down the car window",
    "with shoes by the door still angled from coming home",
    "when the refrigerator hum suddenly becomes clear",
    "with a missed call lying quietly on the screen",
    "after finding a folded paper in an old pocket",
    "when a downstairs door closes and the sound travels far",
    "in the bathroom mirror still fogged after midnight",
    "as someone lowers the volume in the train car",
    "with a sticky note lifting at the corner of the desk",
    "as the billboard outside changes color",
    "while a receipt is held too tightly in line",
    "after the rain stops but the pavement still reflects light",
    "beside an unfinished book near the pillow",
    "as the vending machine drops a cold can",
    "when the breakfast shop downstairs starts steaming",
    "when a late-night message notification sounds once",
    "with a coat still carrying the cold from outside",
    "in the back seat of a quiet taxi",
    "after the door closes and the room slowly settles",
    "when the watch vibrates, but not for the person expected",
    "under a lamp falling across an uncleaned desk",
    "while shower steam has not yet cleared",
    "as the platform announcement repeats itself",
    "with a tissue crumpled in one hand",
    "when keys drop into a bowl with a small sound",
    "as someone rides through a puddle outside the window",
]


EN_OPENING_PATTERNS = [
    "{scene}, the feeling arrives before there is time to explain it.",
    "{scene}, something small suddenly becomes personal.",
    "{scene}, the heart recognizes the moment before the mind does.",
    "{scene}, an ordinary second starts to carry more weight.",
    "{scene}, a listener can step into the feeling without being told how.",
    "{scene}, nothing dramatic has to happen for the emotion to appear.",
    "{scene}, the song feels close to everyday life.",
    "{scene}, the feeling becomes easier to recognize.",
    "{scene}, the room around the listener gets a little quieter.",
    "{scene}, the unsaid part of the feeling moves closer.",
    "{scene}, a small pause can hold more than expected.",
    "{scene}, the lyric meaning feels less like a story and more like a lived moment.",
]


def load_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def pick_index(seed, size, offset=0):
    digest = hashlib.sha256(f"{seed}:{offset}".encode("utf-8")).hexdigest()
    return int(digest[:8], 16) % size


def pick_variant(seed, options, offset=0):
    return options[pick_index(seed, len(options), offset)]


def title_hint(title, english_title, hints):
    text = f"{title} {english_title}".lower()
    for keys, line in hints:
        if any(key.lower() in text for key in keys):
            return line
    return ""


def core_theme(row, lang):
    themes = [theme for theme in (row.get("LyricThemes") or "").split("|") if theme]
    mapping = THEME_CN if lang == "cn" else THEME_EN
    preferred_orders = [
        ("love", "heartbreak"),
        ("memory", "healing"),
        ("heartbreak", "healing"),
        ("love", "memory"),
        ("growth", "healing"),
        ("energy", "personal"),
        ("city-night", "memory"),
    ]
    theme_set = set(themes)
    for first, second in preferred_orders:
        if first in theme_set and second in theme_set:
            connector = "，以及" if lang == "cn" else " and "
            return f"{mapping[first]}{connector}{mapping[second]}"
    if themes:
        return mapping.get(themes[0], "心里那一点没有说完的反应" if lang == "cn" else "the small unsaid reaction inside")
    return "心里那一点没有说完的反应" if lang == "cn" else "the small unsaid reaction inside"


def core_sentence(row, lang, seed):
    core = core_theme(row, lang)
    patterns = CN_CORE_PATTERNS if lang == "cn" else EN_CORE_PATTERNS
    return pick_variant(seed, patterns, 9).format(core=core)


def mood_sentence(row, lang, seed):
    mood_key = row.get("LyricMood", "")
    if lang == "cn":
        options = MOOD_CN_VARIANTS.get(mood_key, ["它没有把情绪讲得很远，只让人想起生活里某个很近的瞬间。"])
    else:
        options = MOOD_EN_VARIANTS.get(mood_key, ["It does not push the feeling far away; it keeps it close to ordinary life."])
    return pick_variant(seed, options, 10)


def energy_sentence(row, lang, seed):
    energy_key = row.get("LyricEnergy", "")
    if lang == "cn":
        options = ENERGY_CN_VARIANTS.get(energy_key, ["所以它可以慢慢进入，不需要把情绪推得太满。"])
    else:
        options = ENERGY_EN_VARIANTS.get(energy_key, ["So it can enter slowly, without making the emotion too large."])
    return pick_variant(seed, options, 11)


def avoid_common_title_words(line, avoid_words):
    if "you" in avoid_words:
        line = line.replace("You may know this kind of moment: ", "Listeners may know this kind of moment: ")
        line = line.replace(" you ", " someone ")
        line = line.replace(" You ", " Someone ")
        line = line.replace(" you.", " someone.")
    if "like" in avoid_words:
        line = line.replace("It feels like ", "It recalls ")
        line = line.replace("it feels like ", "it recalls ")
        line = line.replace("is like ", "recalls ")
        line = line.replace(" like ", " close to ")
        line = line.replace("Like ", "Similar to ")
    if "ordinary" in avoid_words:
        line = line.replace("ordinary", "everyday")
        line = line.replace("Ordinary", "Everyday")
    return line


def line_stem(line):
    return line.rstrip("。.!?")


def line_has_avoid_word(line, avoid_words):
    lower = line.lower()
    return any(re.search(rf"\b{re.escape(word)}\b", lower) for word in avoid_words)


def line_prefix(line, lang):
    if lang == "cn":
        return re.sub(r"[，。；,.;!?！？]", "", line)[:8]
    words = re.findall(r"[A-Za-z']+", line.lower())
    return " ".join(words[:4])


def accept_line(line, used_lines, lang, avoid_words, local_prefixes):
    prefix = line_prefix(line, lang)
    if line in used_lines or line_has_avoid_word(line, avoid_words):
        return False
    if local_prefixes is not None and prefix in local_prefixes:
        return False
    used_lines.add(line)
    if local_prefixes is not None:
        local_prefixes.add(prefix)
    return True


def uniquify_intro_line(line, used_lines, seed, lang, offset, avoid_words=None, local_prefixes=None):
    avoid_words = avoid_words or set()
    line = avoid_common_title_words(line, avoid_words) if lang == "en" else line
    if accept_line(line, used_lines, lang, avoid_words, local_prefixes):
        return line

    details = CN_LINE_DETAILS if lang == "cn" else EN_LINE_DETAILS
    start = pick_index(seed, len(details), offset)
    stem = line_stem(line)

    for attempt in range(len(details) * 12):
        detail = details[(start + attempt) % len(details)]
        if lang == "cn":
            if line.startswith("所以"):
                templates = [
                    "所以开场可以收住一点，让{detail}这样的细节自己说话。",
                    "所以不必把情绪推满，先把{detail}背后的心情交给观众。",
                    "所以让它从{detail}这样的小地方进来，会更自然。",
                    "所以这一段可以留白一点，让{detail}里的心情慢慢出来。",
                    "所以先不要急着推高情绪，把{detail}里的那一下交给现场。",
                    "所以它可以从很小的地方开始，比如{detail}。",
                    "所以让声音先贴近生活，贴近{detail}这样的细节。",
                    "所以这首歌适合慢慢打开，像{detail}带来的那种停顿。",
                    "所以不要急着解释，让{detail}先把人带到情绪里。",
                ]
            elif line.startswith("像"):
                templates = [
                    "像{detail}这样的小细节，也会有这种很轻却很难忽略的感觉。",
                    "人也会被{detail}这样的小细节轻轻停住。",
                    "它更像{detail}之后留下的那点余温。",
                    "这种感觉很像{detail}带来的那一下走神。",
                    "它会让人想到{detail}，不响，却很贴近。",
                    "它像{detail}之后心里没有马上散开的那点反应。",
                    "很多时候，{detail}就足够把人带回那种心情。",
                    "它不需要很大的场面，{detail}这样的小细节就够了。",
                    "听到这里，{detail}那样的画面会自己浮起来。",
                ]
            elif line.startswith("它"):
                templates = [
                    "像{detail}这样的小细节，会让这种情绪变得很近。",
                    "它靠近生活的方式，很像{detail}带来的那一下停顿。",
                    "这种情绪不需要讲得太远，放到{detail}旁边就能明白。",
                    "这种感受放在{detail}里，就会变得很容易代入。",
                    "它真正打动人的地方，藏在{detail}这样的日常里。",
                    "它不是把情绪放大，而是让{detail}这样的细节变得有重量。",
                    "它会让人想起{detail}，也想起自己没说出口的那部分。",
                    "这份情绪很近，近到像{detail}里轻轻晃了一下。",
                    "它把心事放回生活里，放回{detail}这样的地方。",
                ]
            else:
                templates = [
                    "像{detail}这样的生活细节，会把这份心情说得更清楚。",
                    "观众会懂，因为{detail}也藏着同样的反应。",
                    "它离观众不远，就在像{detail}这样的小地方。",
                    "把它放进{detail}这样的场景里，情绪就不再遥远。",
                    "很多人的共鸣，可能就是从{detail}这样的细节开始。",
                    "这种心情很日常，日常到像{detail}一样容易被忽略。",
                    "它不用解释太多，{detail}已经把那份感觉带出来。",
                    "如果说给生活听，它大概会落在{detail}这样的地方。",
                    "观众能走进去，因为{detail}本身就很像生活。",
                ]
            candidate = templates[(attempt // len(details)) % len(templates)].format(stem=stem, detail=detail)
        else:
            if line.startswith("So "):
                templates = [
                    "So the opening can stay simple and let a detail like {detail} do some of the work.",
                    "So there is no need to overstate it; a detail like {detail} can carry the feeling.",
                    "So it can enter through a small detail like {detail}, naturally and without forcing it.",
                    "So this moment can leave space for the feeling behind {detail}.",
                    "So the emotion can begin small, from a detail like {detail}.",
                    "So the voice can stay close to life, close to a detail like {detail}.",
                    "So the song can open slowly, with the pause carried by {detail}.",
                    "So the feeling does not need to be explained before {detail} brings it closer.",
                    "So the room can meet the emotion through something as simple as {detail}.",
                ]
            elif line.startswith("It "):
                templates = [
                    "A small detail like {detail} can carry the same feeling, quietly but clearly.",
                    "This emotion stays close to everyday life through a detail like {detail}.",
                    "The emotion does not need to travel far; a detail like {detail} makes it clear.",
                    "The feeling becomes easier to enter when it is held by {detail}.",
                    "What makes it work is how close it stays to a detail like {detail}.",
                    "It does not need a big scene; {detail} is enough to bring the feeling near.",
                    "A detail like {detail} gives the emotion a place to land.",
                    "The feeling becomes personal through something as small as {detail}.",
                    "It brings the heart back to everyday life, to a detail like {detail}.",
                ]
            else:
                templates = [
                    "A detail like {detail} makes this feeling easier to enter.",
                    "Listeners can understand it through a detail like {detail}.",
                    "It stays close to the audience through a small detail like {detail}.",
                    "The feeling becomes less distant when placed beside {detail}.",
                    "Many people may find their own memory through a detail like {detail}.",
                    "It feels lived-in because it can sit beside {detail}.",
                    "A detail like {detail} keeps the emotion from becoming abstract.",
                    "The audience can step into it through something as simple as {detail}.",
                    "It becomes recognizable through the everyday shape of {detail}.",
                ]
            candidate = templates[(attempt // len(details)) % len(templates)].format(stem=stem, detail=detail)
            candidate = avoid_common_title_words(candidate, avoid_words)

        if accept_line(candidate, used_lines, lang, avoid_words, local_prefixes):
            return candidate

    for attempt in range(len(details) * len(details)):
        first = details[(start + attempt) % len(details)]
        second = details[(start + attempt // len(details) + 11) % len(details)]
        if first == second:
            continue
        if lang == "cn":
            pair_templates = [
                "这份情绪可以从{first}走到{second}，慢慢靠近观众。",
                "从{first}到{second}，生活里的小反应会把它说清楚。",
                "它不需要夸张，只要让{first}和{second}之间的心情浮出来。",
                "观众会在{first}和{second}之间，找到自己的那一点共鸣。",
            ]
        else:
            pair_templates = [
                "The feeling can move from {first} to {second} without becoming forced.",
                "Between {first} and {second}, the emotion has enough room to feel lived-in.",
                "It does not need to be overstated; {first} and {second} can bring it close.",
                "Listeners can find their own memory somewhere between {first} and {second}.",
            ]
        candidate = pair_templates[(attempt // len(details)) % len(pair_templates)].format(first=first, second=second)
        if lang == "en":
            candidate = avoid_common_title_words(candidate, avoid_words)
        if accept_line(candidate, used_lines, lang, avoid_words, local_prefixes):
            return candidate

    for attempt in range(len(details) * len(details) * len(details)):
        first = details[(start + attempt) % len(details)]
        second = details[(start + attempt // len(details) + 11) % len(details)]
        third = details[(start + attempt // (len(details) * len(details)) + 19) % len(details)]
        if len({first, second, third}) < 3:
            continue
        if lang == "cn":
            triple_templates = [
                "从{first}，到{second}，再到{third}，这份心情会一点点走近。",
                "它可以很轻地经过{first}、{second}和{third}，让观众自己接住。",
                "把{first}、{second}和{third}放在一起，那份情绪就有了生活的温度。",
            ]
        else:
            triple_templates = [
                "From {first} to {second} and then {third}, the feeling can move closer without being forced.",
                "It can pass lightly through {first}, {second}, and {third}, leaving listeners room to meet it.",
                "Placed among {first}, {second}, and {third}, the emotion keeps the temperature of everyday life.",
            ]
        candidate = triple_templates[(attempt // (len(details) * len(details))) % len(triple_templates)].format(
            first=first, second=second, third=third
        )
        if lang == "en":
            candidate = avoid_common_title_words(candidate, avoid_words)
        if accept_line(candidate, used_lines, lang, avoid_words, local_prefixes):
            return candidate

    fallback = f"{stem}." if lang == "en" else f"{stem}。"
    used_lines.add(fallback)
    if local_prefixes is not None:
        local_prefixes.add(line_prefix(fallback, lang))
    return fallback


def clean_title(row):
    title = row["ChineseDisplayTitle"] or row["Song"]
    title = re.sub(r"\s*\([^)]*\)", "", title)
    title = re.sub(r"\s*（[^）]*）", "", title)
    return title.strip() or row["Song"]


def unique_chinese_opening(seed, used):
    scene_start = pick_index(seed, len(CN_SCENES), 1)
    ending_start = pick_index(seed, len(CN_OPENING_ENDINGS), 2)
    for attempt in range(len(CN_SCENES) * len(CN_OPENING_ENDINGS)):
        scene = CN_SCENES[(scene_start + attempt) % len(CN_SCENES)]
        ending = CN_OPENING_ENDINGS[(ending_start + attempt * 3) % len(CN_OPENING_ENDINGS)]
        opening = f"{scene}，{ending}"
        if opening not in used:
            used.add(opening)
            return opening
    opening = f"{CN_SCENES[scene_start]}，{CN_OPENING_ENDINGS[ending_start]}"
    return opening


def unique_english_opening(seed, used, avoid_words):
    scene_start = pick_index(seed, len(EN_SCENES), 1)
    pattern_start = pick_index(seed, len(EN_OPENING_PATTERNS), 2)
    for attempt in range(len(EN_SCENES) * len(EN_OPENING_PATTERNS)):
        scene = EN_SCENES[(scene_start + attempt) % len(EN_SCENES)]
        pattern = EN_OPENING_PATTERNS[(pattern_start + attempt * 3) % len(EN_OPENING_PATTERNS)]
        opening = pattern.format(scene=scene)
        opening = opening[:1].upper() + opening[1:]
        lower = opening.lower()
        if opening not in used and not any(re.search(rf"\b{re.escape(word)}\b", lower) for word in avoid_words):
            used.add(opening)
            return opening
    opening = EN_OPENING_PATTERNS[pattern_start].format(scene=EN_SCENES[scene_start])
    opening = opening[:1].upper() + opening[1:]
    used.add(opening)
    return opening


def chinese_intro(row, used_lines):
    seed = f"{row['Year']}-{row['Rank']}-{row['Song']}-life"
    hint = title_hint(clean_title(row), row["EnglishDisplayTitle"], TITLE_CN_HINTS)
    mood = mood_sentence(row, "cn", seed)
    energy = energy_sentence(row, "cn", seed)

    if hint:
        second = hint
    else:
        second = core_sentence(row, "cn", seed)

    opening = unique_chinese_opening(seed, used_lines)
    local_prefixes = {line_prefix(opening, "cn")}
    lines = [second, mood, energy]
    return "\n".join(
        [opening]
        + [
            uniquify_intro_line(line, used_lines, seed, "cn", 20 + index, local_prefixes=local_prefixes)
            for index, line in enumerate(lines)
        ]
    )


def english_intro(row, used_lines):
    seed = f"{row['Year']}-{row['Rank']}-{row['Song']}-life"
    hint = title_hint(clean_title(row), row["EnglishDisplayTitle"], TITLE_EN_HINTS)
    mood = mood_sentence(row, "en", seed)
    energy = energy_sentence(row, "en", seed)
    english_title = (row.get("EnglishDisplayTitle") or "").strip().lower()
    avoid_words = {english_title} if english_title in {"like", "you", "ordinary"} else set()

    if hint:
        second = hint
    else:
        second = core_sentence(row, "en", seed)

    if "you" in avoid_words:
        second = second.replace("You may know that kind of moment too: ", "Listeners may know that kind of moment too: ")
        second = second.replace("you", "someone")
        second = second.replace("You", "Someone")
    if "like" in avoid_words:
        second = second.replace("It feels like ", "It recalls ")
        second = second.replace(" like ", " close to ")
    if "ordinary" in avoid_words:
        second = second.replace("ordinary", "everyday")
        mood = mood.replace("ordinary", "daily")

    opening = unique_english_opening(seed, used_lines, avoid_words)
    local_prefixes = {line_prefix(opening, "en")}
    lines = [second, mood, energy]
    return "\n".join(
        [opening]
        + [
            uniquify_intro_line(line, used_lines, seed, "en", 30 + index, avoid_words, local_prefixes)
            for index, line in enumerate(lines)
        ]
    )


def visible_time_lines(row):
    if row.get("MovedBackSameSinger") == "Yes":
        return [row["SameSingerLineWithDate"]]
    lines = []
    if row["CoverVersionLineEnglish"]:
        lines.append(row["CoverVersionLineEnglish"])
    lines.append(row["OriginalLineEnglish"])
    return lines


def main():
    rows = load_csv(SOURCE_CSV)
    used_cn_openings = set()
    used_en_openings = set()

    for row in rows:
        row["ChineseIntroLifeLike"] = chinese_intro(row, used_cn_openings)
        row["EnglishIntroLifeLike"] = english_intro(row, used_en_openings)

    lines = [
        "# Song Intros by Year - Same Singer Moved Back v12 Life Like Relatable",
        "",
        "Chinese intro appears before English intro. Intros connect lyric-derived meaning with relatable everyday moments, without quoting lyrics or repeating song titles.",
        "",
    ]

    current_year = None
    for row in rows:
        if row["Year"] != current_year:
            current_year = row["Year"]
            lines.extend(["", f"## {current_year}"])

        lines.extend(["", f"### {row['Year']}.{int(row['Rank']):02d}"])
        lines.extend(row["ChineseIntroLifeLike"].splitlines())
        lines.append("")
        lines.extend(row["EnglishIntroLifeLike"].splitlines())
        lines.append("")
        if row["ChineseDisplayTitle"]:
            lines.append(row["ChineseDisplayTitle"])
        lines.append(row["EnglishDisplayTitle"])
        lines.append("by")
        lines.extend(visible_time_lines(row))

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    fieldnames = []
    for row in rows:
        for name in row.keys():
            if name not in OBSOLETE_INTRO_FIELDS and name not in fieldnames:
                fieldnames.append(name)
    output_rows = [{name: row.get(name, "") for name in fieldnames} for row in rows]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    by_year = defaultdict(int)
    for row in rows:
        by_year[row["Year"]] += 1
    print(f"wrote {OUT_MD}")
    print(f"wrote {OUT_CSV}")
    print(f"rows: {len(rows)}")
    print(dict(sorted(by_year.items())))


if __name__ == "__main__":
    main()
