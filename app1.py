import streamlit as st
import time
import json
import os

# ページ設定
st.set_page_config(page_title="持ち物チェックリスト", page_icon="🧳", layout="centered")

# --- スマホ対応CSS ---
st.markdown("""
<style>
/* チェックボックスのタップ領域・サイズを大きく */
.stCheckbox label {
    padding: 10px 4px !important;
    font-size: 17px !important;
    line-height: 1.4 !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    cursor: pointer;
}
.stCheckbox label span {
    font-size: 17px !important;
}
/* チェックボックス本体を大きく（スマホ最適化: 24px） */
.stCheckbox input[type="checkbox"] {
    width: 24px !important;
    height: 24px !important;
    min-width: 24px !important;
}
/* ゴミ箱ボタンを小さくコンパクトに */
[data-testid="column"]:last-child .stButton button {
    padding: 2px 6px !important;
    font-size: 16px !important;
    min-height: 36px !important;
    width: 100% !important;
    background: transparent !important;
    border: none !important;
}
/* 全ボタンのタップ領域確保 */
.stButton button {
    min-height: 44px !important;
}

/* スマホでの縦積みを防ぎ、項目とゴミ箱を1行に収める */
.streamlit-expanderContent [data-testid="stHorizontalBlock"] {
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: center !important;
    gap: 0px !important;
}
/* 項目の列は残り幅いっぱいを使う */
.streamlit-expanderContent [data-testid="column"]:first-child {
    flex: 1 1 auto !important;
    width: 100% !important;
}
/* ゴミ箱の列は幅を固定する */
.streamlit-expanderContent [data-testid="column"]:last-child {
    flex: 0 0 40px !important;
    width: 40px !important;
    min-width: 40px !important;
}

/* expanderの内側パディング調整 */
.streamlit-expanderContent {
    padding: 4px 8px !important;
}
/* モバイルでフォントサイズ調整 */
@media (max-width: 600px) {
    .stCheckbox label {
        font-size: 15px !important;
    }
    h1 { font-size: 1.4rem !important; }
    h2 { font-size: 1.1rem !important; }
}
</style>
""", unsafe_allow_html=True)

# --- データ保存用の設定 ---
DATA_FILE = "packing_users_data.json"

def load_all_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_current_state():
    if st.session_state.get("current_user"):
        data = load_all_data()
        data[st.session_state["current_user"]] = {
            "items": st.session_state["items"],
            "categories": st.session_state["categories"],
            "mode": st.session_state["mode"],
            "gender": st.session_state["gender"],
            "nights": st.session_state["nights"],
            "transportOut": st.session_state["transportOut"],
            "transportRet": st.session_state["transportRet"],
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# --- マスターデータ定義 ---
MASTER_ITEMS = [
    {'id': '1', 'name': '財布', 'category': 'essentials', 'tags': ['common']},
    {'id': '2', 'name': '交通系ICカード', 'category': 'essentials', 'tags': ['common']},
    {'id': '3', 'name': '学生証', 'category': 'essentials', 'tags': ['common']},
    {'id': 'add1', 'name': 'スマホ', 'category': 'essentials', 'tags': ['common']},
    {'id': 'add2', 'name': '保険証', 'category': 'essentials', 'tags': ['common']},
    {'id': 'tr_shin_out', 'name': '新幹線のチケット(行き)', 'category': 'essentials', 'tags': ['transport_shinkansen_out']},
    {'id': 'tr_shin_ret', 'name': '新幹線のチケット(帰り)', 'category': 'essentials', 'tags': ['transport_shinkansen_return']},
    {'id': 'tr_plane_out', 'name': '航空券/eチケット(行き)', 'category': 'essentials', 'tags': ['transport_plane_out']},
    {'id': 'tr_plane_ret', 'name': '航空券/eチケット(帰り)', 'category': 'essentials', 'tags': ['transport_plane_return']},
    {'id': 'tr_bus_out', 'name': 'バス乗車票/予約画面(行き)', 'category': 'essentials', 'tags': ['transport_bus_out']},
    {'id': 'tr_bus_ret', 'name': 'バス乗車票/予約画面(帰り)', 'category': 'essentials', 'tags': ['transport_bus_return']},
    {'id': 'tr_car_1', 'name': '運転免許証', 'category': 'essentials', 'tags': ['transport_car_any']},
    {'id': 'tr_car_2', 'name': 'ETCカード', 'category': 'essentials', 'tags': ['transport_car_any']},
    {'id': 'tr_car_3', 'name': '車の鍵', 'category': 'essentials', 'tags': ['transport_car_any']},
    {'id': 'live1', 'name': 'ライブチケット(電子/紙)', 'category': 'live_goods', 'tags': ['live']},
    {'id': 'live2', 'name': '本人確認書類(顔写真付)', 'category': 'live_goods', 'tags': ['live']},
    {'id': 'live3', 'name': 'FC会員証', 'category': 'live_goods', 'tags': ['live']},
    {'id': 'live4', 'name': 'ペンライト', 'category': 'live_goods', 'tags': ['live']},
    {'id': 'live5', 'name': '交換用電池', 'category': 'live_goods', 'tags': ['live']},
    {'id': 'live6', 'name': 'マフラータオル', 'category': 'live_goods', 'tags': ['live']},
    {'id': 'live7', 'name': '双眼鏡', 'category': 'live_goods', 'tags': ['live']},
    {'id': 'live9', 'name': 'ライブTシャツ', 'category': 'clothing', 'tags': ['live']},
    {'id': '6', 'name': '服(上)', 'category': 'clothing', 'tags': ['common'], 'autoCount': True},
    {'id': '7', 'name': '服(下)', 'category': 'clothing', 'tags': ['common'], 'autoCount': True},
    {'id': '8', 'name': 'パンツ', 'category': 'clothing', 'tags': ['common'], 'autoCount': True},
    {'id': '9', 'name': 'シャツ(肌着)', 'category': 'clothing', 'tags': ['common'], 'autoCount': True},
    {'id': '10', 'name': '靴下', 'category': 'clothing', 'tags': ['common'], 'autoCount': True},
    {'id': '11', 'name': '部屋着(上)', 'category': 'clothing', 'tags': ['common']},
    {'id': '12', 'name': '部屋着(下)', 'category': 'clothing', 'tags': ['common']},
    {'id': '13', 'name': 'サングラス', 'category': 'clothing', 'tags': ['common']},
    {'id': 'f_cloth1', 'name': 'ストッキング/タイツ(予備)', 'category': 'clothing', 'tags': ['female']},
    {'id': 'f_cloth2', 'name': 'ブラジャー', 'category': 'clothing', 'tags': ['female'], 'autoCount': True},
    {'id': 'f_cloth3', 'name': 'キャミソール', 'category': 'clothing', 'tags': ['female'], 'autoCount': True},
    {'id': '21', 'name': '歯ブラシ', 'category': 'grooming', 'tags': ['common']},
    {'id': '19', 'name': 'コンタクト', 'category': 'grooming', 'tags': ['common']},
    {'id': '20', 'name': 'メガネ', 'category': 'grooming', 'tags': ['common']},
    {'id': '24', 'name': '薬', 'category': 'grooming', 'tags': ['common']},
    {'id': '25', 'name': '体洗うタオル', 'category': 'grooming', 'tags': ['common']},
    {'id': '18', 'name': 'トラベルセット', 'category': 'grooming', 'tags': ['common']},
    {'id': 'add3', 'name': 'マスク', 'category': 'grooming', 'tags': ['common']},
    {'id': '14', 'name': 'メイク道具一式', 'category': 'grooming', 'tags': ['female']},
    {'id': 'f_groom1', 'name': 'クレンジング', 'category': 'grooming', 'tags': ['female']},
    {'id': '15', 'name': 'ヘアアイロン', 'category': 'grooming', 'tags': ['female']},
    {'id': '16', 'name': 'ナプキン', 'category': 'grooming', 'tags': ['female']},
    {'id': '17', 'name': '化粧水・乳液', 'category': 'grooming', 'tags': ['female']},
    {'id': '22', 'name': 'ケープ', 'category': 'grooming', 'tags': ['female']},
    {'id': '23', 'name': 'ヘアオイル', 'category': 'grooming', 'tags': ['female']},
    {'id': 'f_groom2', 'name': 'ヘアゴム/シュシュ', 'category': 'grooming', 'tags': ['female']},
    {'id': 'f_groom3', 'name': 'アクセサリー', 'category': 'grooming', 'tags': ['female']},
    {'id': 'f_groom4', 'name': '日焼け止め', 'category': 'grooming', 'tags': ['female']},
    {'id': 'm_groom1', 'name': '髭剃り/シェーバー', 'category': 'grooming', 'tags': ['male']},
    {'id': 'm_groom2', 'name': 'シェービングフォーム', 'category': 'grooming', 'tags': ['male']},
    {'id': 'm_groom3', 'name': 'ワックス/整髪料', 'category': 'grooming', 'tags': ['male']},
    {'id': 'm_groom4', 'name': '洗顔料', 'category': 'grooming', 'tags': ['male']},
    {'id': 'm_groom5', 'name': '汗拭きシート', 'category': 'grooming', 'tags': ['male']},
    {'id': '26', 'name': '充電器', 'category': 'gadgets', 'tags': ['common']},
    {'id': '27', 'name': 'モバイルバッテリー', 'category': 'gadgets', 'tags': ['common']},
    {'id': '28', 'name': 'イヤホン', 'category': 'gadgets', 'tags': ['common']},
    {'id': '29', 'name': 'ケーブル', 'category': 'gadgets', 'tags': ['common']},
    {'id': '32', 'name': 'ハンカチ', 'category': 'others', 'tags': ['common'], 'autoCount': True},
    {'id': '33', 'name': 'タオル', 'category': 'others', 'tags': ['common']},
    {'id': '34', 'name': 'ペットボトルホルダー', 'category': 'others', 'tags': ['common']},
    {'id': '35', 'name': 'おりたたみ傘', 'category': 'others', 'tags': ['common']},
    {'id': '37', 'name': 'ウエットティッシュ', 'category': 'others', 'tags': ['common']},
    {'id': 'add4', 'name': 'ビニール袋', 'category': 'others', 'tags': ['common']},
]

INITIAL_CATEGORIES = {
    'live_goods': {'label': 'ライブグッズ・必需品', 'icon': '🎫'},
    'essentials': {'label': '必需品・貴重品', 'icon': '🧳'},
    'clothing': {'label': '衣類', 'icon': '👕'},
    'grooming': {'label': '美容・洗面', 'icon': '✨'},
    'gadgets': {'label': 'ガジェット', 'icon': '📱'},
    'others': {'label': 'その他', 'icon': '📦'},
}

TRANSPORT_OPTIONS = {
    'shinkansen': '新幹線 🚅',
    'plane': '飛行機 ✈️',
    'bus': '高速バス 🚌',
    'car': '車 🚗',
    'train': '電車/他 🚃'
}

# --- コールバック関数 ---
def uncheck_all():
    for item in st.session_state["items"]:
        item['checked'] = False
    for key in list(st.session_state.keys()):
        if key.startswith(f"chk_{st.session_state['current_user']}_"):
            st.session_state[key] = False
    save_current_state()

def do_reset_user_data():
    """実際にリセットを実行する"""
    if st.session_state.get("current_user"):
        st.session_state["items"] = [{"checked": False, **item} for item in MASTER_ITEMS]
        st.session_state["categories"] = INITIAL_CATEGORIES.copy()
        for key in list(st.session_state.keys()):
            if key.startswith(f"chk_{st.session_state['current_user']}_"):
                st.session_state[key] = False
        st.session_state["confirm_reset"] = False
        save_current_state()

def request_reset():
    """確認ダイアログを表示するフラグを立てる"""
    st.session_state["confirm_reset"] = True

def cancel_reset():
    st.session_state["confirm_reset"] = False

def add_custom_item():
    name = st.session_state.get("new_item_name", "").strip()
    cat = st.session_state.get("new_item_cat")
    if name and cat:
        st.session_state["items"].append({
            'id': f"custom_{int(time.time())}",
            'name': name,
            'category': cat,
            'tags': ['common'],
            'checked': False,
            'autoCount': False
        })
        st.session_state["new_item_name"] = ""
        save_current_state()

def delete_item(item_id):
    st.session_state["items"] = [item for item in st.session_state["items"] if item['id'] != item_id]
    chk_key = f"chk_{st.session_state['current_user']}_{item_id}"
    if chk_key in st.session_state:
        del st.session_state[chk_key]
    save_current_state()


st.title("持ち物チェックリスト 🧳")

# --- ユーザー切り替え・ログインエリア ---
with st.container(border=True):
    col_user1, col_user2 = st.columns([3, 1])
    all_data = load_all_data()

    with col_user1:
        input_user = st.text_input("使う人の名前を入力", placeholder="例: ママ、パパ、〇〇")

    with col_user2:
        st.write("")
        st.write("")
        if not input_user:
            btn_text = "名前を入力..."
            is_disabled = True
        elif input_user in all_data:
            btn_text = "🔄 続きから"
            is_disabled = False
        else:
            btn_text = "✨ 新規作成"
            is_disabled = False
        login_btn = st.button(btn_text, disabled=is_disabled)

    if login_btn and input_user:
        st.session_state["current_user"] = input_user
        st.session_state["confirm_reset"] = False
        if input_user in all_data:
            user_data = all_data[input_user]
            st.session_state["items"] = user_data.get("items", [{"checked": False, **item} for item in MASTER_ITEMS])
            st.session_state["categories"] = user_data.get("categories", INITIAL_CATEGORIES.copy())
            st.session_state["mode"] = user_data.get("mode", 'normal')
            st.session_state["gender"] = user_data.get("gender", 'female')
            st.session_state["nights"] = user_data.get("nights", 1)
            st.session_state["transportOut"] = user_data.get("transportOut", 'shinkansen')
            st.session_state["transportRet"] = user_data.get("transportRet", 'shinkansen')
            st.success(f"おかえりなさい、{input_user}さん！前回の続きからスタートします。")
        else:
            st.session_state["items"] = [{"checked": False, **item} for item in MASTER_ITEMS]
            st.session_state["categories"] = INITIAL_CATEGORIES.copy()
            st.session_state["mode"] = 'normal'
            st.session_state["gender"] = 'female'
            st.session_state["nights"] = 1
            st.session_state["transportOut"] = 'shinkansen'
            st.session_state["transportRet"] = 'shinkansen'
            st.info(f"はじめまして、{input_user}さん！新しいリストを作成しました。")
            save_current_state()

if not st.session_state.get("current_user"):
    st.stop()

st.write(f"👤 **現在表示中:** {st.session_state['current_user']} さんのリスト")

# --- ヘッダー・設定エリア ---
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        mode_radio = st.radio("シーン", ["🧳 旅行", "🎵 ライブ"], horizontal=True, index=0 if st.session_state["mode"] == 'normal' else 1)
        new_mode = 'normal' if '旅行' in mode_radio else 'live'
        if new_mode != st.session_state["mode"]:
            st.session_state["mode"] = new_mode
            save_current_state()
            st.rerun()

    with col2:
        gender_radio = st.radio("性別", ["👩 女性", "👨 男性"], horizontal=True, index=0 if st.session_state["gender"] == 'female' else 1)
        new_gender = 'female' if '女性' in gender_radio else 'male'
        if new_gender != st.session_state["gender"]:
            st.session_state["gender"] = new_gender
            save_current_state()
            st.rerun()

    st.divider()

    col3, col4, col5 = st.columns([1, 1, 1])
    with col3:
        new_nights = st.number_input("宿泊数", min_value=1, max_value=10, value=st.session_state["nights"])
        if new_nights != st.session_state["nights"]:
            st.session_state["nights"] = new_nights
            save_current_state()
            st.rerun()
    with col4:
        new_out = st.selectbox("行き", list(TRANSPORT_OPTIONS.keys()), format_func=lambda x: TRANSPORT_OPTIONS[x], index=list(TRANSPORT_OPTIONS.keys()).index(st.session_state["transportOut"]))
        if new_out != st.session_state["transportOut"]:
            st.session_state["transportOut"] = new_out
            save_current_state()
            st.rerun()
    with col5:
        new_ret = st.selectbox("帰り", list(TRANSPORT_OPTIONS.keys()), format_func=lambda x: TRANSPORT_OPTIONS[x], index=list(TRANSPORT_OPTIONS.keys()).index(st.session_state["transportRet"]))
        if new_ret != st.session_state["transportRet"]:
            st.session_state["transportRet"] = new_ret
            save_current_state()
            st.rerun()

# --- 表示アイテムのフィルタリング ---
displayed_items = []
for item in st.session_state["items"]:
    tags = item.get('tags', [])
    if 'female' in tags and st.session_state["gender"] != 'female': continue
    if 'male' in tags and st.session_state["gender"] != 'male': continue
    is_transport = any(t.startswith('transport_') for t in tags)
    if is_transport:
        if f"transport_{st.session_state['transportOut']}_out" in tags: pass
        elif f"transport_{st.session_state['transportRet']}_return" in tags: pass
        elif 'transport_car_any' in tags and (st.session_state["transportOut"] == 'car' or st.session_state["transportRet"] == 'car'): pass
        else: continue
    if st.session_state["mode"] != 'live' and 'live' in tags: continue
    displayed_items.append(item)

# --- プログレスバー ---
total_count = len(displayed_items)
checked_count = sum(1 for item in displayed_items if item['checked'])
progress_val = int((checked_count / total_count * 100)) if total_count > 0 else 0

col_prog_1, col_prog_2 = st.columns([3, 2])
with col_prog_1:
    st.progress(progress_val / 100, text=f"準備状況: {progress_val}%")
with col_prog_2:
    st.button("🔄 チェックをすべて外す", on_click=uncheck_all)

if progress_val == 100 and total_count > 0:
    msg = "準備完了！ライブ楽しんで！🎉" if st.session_state["mode"] == 'live' else "準備完了！良い旅を！✨"
    st.success(msg)

st.write("")

# --- チェックリスト本体 ---
def toggle_item(item_id, key_name):
    new_status = st.session_state[key_name]
    for item in st.session_state["items"]:
        if item['id'] == item_id:
            item['checked'] = new_status
            break
    save_current_state()

for cat_key, cat_info in st.session_state["categories"].items():
    if cat_key == 'live_goods' and st.session_state["mode"] != 'live': continue
    cat_items = [i for i in displayed_items if i['category'] == cat_key]
    if not cat_items and not cat_key.startswith('custom_'): continue

    cat_checked = sum(1 for i in cat_items if i['checked'])
    cat_total = len(cat_items)

    with st.expander(f"{cat_info['icon']} **{cat_info['label']}** ({cat_checked}/{cat_total})", expanded=True):
        if not cat_items:
            st.caption("アイテムがありません")

        for item in cat_items:
            col_item, col_del = st.columns([0.88, 0.12])
            display_name = f"{item['name']} ×{st.session_state['nights']}" if item.get('autoCount') else item['name']
            box_key = f"chk_{st.session_state['current_user']}_{item['id']}"

            with col_item:
                st.checkbox(
                    display_name,
                    value=item['checked'],
                    key=box_key,
                    on_change=toggle_item,
                    args=(item['id'], box_key)
                )
            with col_del:
                del_btn_key = f"del_{st.session_state['current_user']}_{item['id']}"
                st.button("🗑️", key=del_btn_key, on_click=delete_item, args=(item['id'],), help="削除")

# --- アイテム追加エリア ---
st.write("---")
with st.container(border=True):
    st.subheader("➕ アイテムを追加")
    col_add1, col_add2 = st.columns([2, 1])
    with col_add1:
        st.text_input("アイテム名", key="new_item_name")
    with col_add2:
        valid_categories = {k: v for k, v in st.session_state["categories"].items() if not (k == 'live_goods' and st.session_state["mode"] != 'live')}
        st.selectbox("カテゴリー", list(valid_categories.keys()), format_func=lambda x: valid_categories[x]['label'], key="new_item_cat")
    st.button("追加する", type="primary", on_click=add_custom_item)

st.write("")

# --- 初期化ボタン（確認ダイアログ付き） ---
if not st.session_state.get("confirm_reset", False):
    st.button("🚨 このユーザーのデータを初期化", type="secondary", on_click=request_reset)
else:
    with st.container(border=True):
        st.warning("⚠️ **本当に初期化しますか？**\nチェック状態・追加アイテムがすべてリセットされます。この操作は元に戻せません。")
        col_yes, col_no = st.columns(2)
        with col_yes:
            st.button("✅ はい、初期化する", type="primary", on_click=do_reset_user_data)
        with col_no:
            st.button("❌ キャンセル", on_click=cancel_reset)