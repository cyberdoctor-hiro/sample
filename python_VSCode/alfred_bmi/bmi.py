# from IPython import get_ipython
# from IPython.display import display
# %%
import sys
import json


def split_query(q):
    splited = q.split()
    if len(splited) == 1:
        return (float(splited[0]), 0)             # float()でエラーが起きたときの処理を追加すべき
    elif len(splited) == 2:
        return (float(splited[0]), float(splited[1]))
    else:
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
        ht_wt = split_query(q)
    except ValueError:
        ht_wt = None

    if ht_wt:
        ht, wt = ht_wt
        bmi = round(wt / (ht / 100)**2, 1) if wt != 0 else 0
        ob = round((ht / 100)**2 * 25, 1)
        std = round((ht / 100)**2 * 22, 1)
        low = round((ht / 100)**2 * 18.5, 1)

        if wt == 0:
            title = f"肥満: {ob}, 標準: {std}, 低体重: {low}"
            subtitle = f"身長: {ht}"
            arg = subtitle + ", " + title
            results = [create_json("ht", title, subtitle, arg, True)]
        else:
            title = f"BMI: {bmi}, 肥満: {ob}, 標準: {std}, 低体重: {low}"
            subtitle = f"身長: {ht}, 体重: {wt}"
            arg = subtitle + ", " + title
            results = [create_json("ht", title, subtitle, arg, True)]
    else:
        title = "無効な入力"
        subtitle = "数値を入力してください"
        arg = q
        results = [create_json("invalid", title, subtitle, q, False)]

    sys.stdout.write(json.dumps({"items": results}, ensure_ascii=False))


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    main(query)
