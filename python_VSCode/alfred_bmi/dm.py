import sys
import json


def split_query(q):
    splited = q.split()
    try:
        if len(splited) == 1:
            return (float(splited[0]), 0, 0)
        elif len(splited) == 2:
            return (float(splited[0]), float(splited[1]), 0)
        elif len(splited) == 3:
            return(float(splited[0]), float(splited[1]), float(splited[2]))
        else:
            return None
    except ValueError:
        return None


def create_json(uid, title, subtitle, arg, valid):
    return {
        "uid": uid,
        "title": title,
        "subtitle": subtitle,
        "arg": arg,
        "valid": valid
    }


def main(q):
    try:
        ht_age_act = split_query(q)      # 身長、年齢、活動
    except ValueError:
        ht_age_act = None

    ht, act, age = (0.0, 0.0, 0.0)
    act_cal = {"1": 27.5, "2": 32.5, "3": 37.5}
    act_mean = {"1": "軽度", "2": "普通", "3": "重度"}

    try:
        if len(ht_age_act) == 1:
            ht = float(ht_age_act[0])
            std = (ht/100) ** 2 * 22
            t = f"標準体重:{std}"
            s = f"身長:{ht}, 活動(1:デスクワーク、2:立ち仕事、3:力仕事), 年齢"
            a = f"身長:{ht}, {t}"
            r = [create_json("ht", t, s, a, True)]
        elif len(ht_age_act) == 2:
            ht, act = float(ht_age_act[0]), ht_age_act[1]
            std = (ht/100) ** 2 * 22
            cal = std * act_cal[act]
            t = f"標準体重:{std}, カロリー:{cal}"
            s = f"身長:{ht}, 活動:{act_mean[act]}, 年齢"
            a = f"身長:{ht}, 活動:{act_mean[act]}, {t}"
            r = [create_json("ht,act", t, s, a, True)]
        elif len(ht_age_act) == 3:
            ht, act, age = float(ht_age_act[0]), ht_age_act[1], float(ht_age_act[2])
            std = (ht/100) ** 2 * (22 if age < 65 else 23.5)
            cal = std * act_cal[act]
            t = f"標準体重:{std}, カロリー:{cal}"
            s = f"身長:{ht}, 活動:{act_mean[act]}, 年齢:{age}"
            a = f"身長:{ht}, 活動:{act_mean[act]}, {t}"
            r = [create_json("ht,act,age", t, s, a, True)]
        else:
            raise ValueError
    except ValueError:
        t = "Error!"
        s = "身長, 活動(1:デスクワーク、2:立ち仕事、3:力仕事), 年齢"
        a = ""
        r = [create_json("invalid", t, s, a, False)]
        
    sys.stdout.write(json.dumps({"items": r}, ensure_ascii=False))


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    main(query)
