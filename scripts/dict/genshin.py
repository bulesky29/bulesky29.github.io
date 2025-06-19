import requests
import json
from datetime import datetime

# 数据源 URL
DATA_URL = "https://dataset.genshin-dictionary.com/words.json"

def fetch_genshin_data(url):
    """
    从指定的 URL 获取 JSON 数据。
    """
    try:
        print("正在从 URL 获取数据...")
        response = requests.get(url, timeout=30)
        # 如果请求失败，则抛出 HTTPError 异常
        response.raise_for_status()
        print("数据获取成功！")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"错误：无法获取数据。 {e}")
        return None

def build_explanation_html(item):
    """
    为单个词条构建 HTML 格式的解释字符串。
    这个解释对该词条的所有语言版本（中/日/英）都是通用的。
    """
    # 使用 <div> 容器包裹整个解释，方便样式控制
    html = '<div>'

    # --- 词条和发音 ---
    ja_word = item.get('ja', 'N/A')
    pronunciation = item.get('pronunciationJa', '')
    html += f'<h2>{ja_word}</h2>'
    if pronunciation:
        html += f'<blockquote>发音(日): {pronunciation}</blockquote>'

    html += '<hr>'

    # --- 各语言对应词 ---
    html += '<b>对照</b><br>'
    html += f"• <b>English:</b> {item.get('en', 'N/A')}<br>"
    html += f"• <b>简体中文:</b> {item.get('zhCN', 'N/A')}<br>"
    html += f"• <b>繁體中文:</b> {item.get('zhTW', 'N/A')}<br>"

    # --- 注释 ---
    notes_zh = item.get('notesZh', '').strip()
    if notes_zh:
        # 将换行符替换为 <br>
        notes_zh_html = notes_zh.replace('\n', '<br>')
        html += f"<br><b>中文注释:</b><br><blockquote>{notes_zh_html}</blockquote>"

    notes_ja = item.get('notes', '').strip()
    if notes_ja:
        notes_ja_html = notes_ja.replace('\n', '<br>')
        html += f"<br><b>日语注释:</b><br><blockquote>{notes_ja_html}</blockquote>"

    # --- 例句 ---
    examples = item.get('examples', [])
    if examples:
        html += '<hr><b>例句:</b><br>'
        for i, ex in enumerate(examples):
            if i > 0:
                html += '<br>' # 在例句之间添加一些间距
            en_ex = ex.get('en', '')
            ja_ex = ex.get('ja', '')
            ref = ex.get('ref', '')

            if ja_ex:
                html += f"• {ja_ex}<br>"
            if en_ex:
                html += f"• {en_ex}<br>"
            if ref:
                # 使用 <i> 标签显示斜体出处
                html += f"&nbsp;&nbsp;<i>(出处: {ref})</i><br>"
    
    # --- 标签 ---
    tags = item.get('tags', [])
    if tags:
        html += '<hr>'
        html += f"<b>标签:</b> {' / '.join(tags)}"

    html += '</div>'
    return html

def create_dictionary_file(data):
    """
    根据处理好的数据生成最终的字典文本文件。
    """
    if not data:
        print("没有数据，无法创建文件。")
        return

    print("正在生成词典条目...")
    entries = []
    
    for item in data:
        # 为每个词条创建一个通用的、详细的HTML解释
        explanation = build_explanation_html(item)

        # 创建一个集合来存放所有可能的词头，以避免重复
        headwords = set()

        # 1. 添加各种语言的词头
        #    处理用 " / " 分隔的多个词形
        for lang_key in ['en', 'ja', 'zhCN', 'zhTW']:
            if item.get(lang_key):
                # .split('/') 会将 "A / B" 分割成 ['A ', ' B']，用 strip() 去除空格
                words = [w.strip() for w in item[lang_key].split('/')]
                headwords.update(words)

        # 2. 添加日文变体
        if 'variants' in item and 'ja' in item['variants']:
            headwords.update(item['variants']['ja'])

        # 3. 为每个词头创建一行 "词头@解释"
        for word in headwords:
            if word:  # 确保词头不是空字符串
                # 在将解释添加到条目前，替换掉解释本身可能包含的换行符
                # 虽然 build_explanation_html 内部已经处理了，这里是双重保险
                cleaned_explanation = explanation.replace('\n', '').replace('\r', '')
                entries.append(f"{word}@{cleaned_explanation}")

    # --- 文件写入 ---
    today_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"genshin-dict-{today_str}.txt"
    
    print(f"正在将 {len(entries)} 个条目写入文件: {filename} ...")
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # 使用 '\n' 将所有条目连接起来写入文件
            f.write('\n'.join(entries))
        print("文件创建成功！")
        print(f"文件路径: ./{filename}")
    except IOError as e:
        print(f"错误：无法写入文件。{e}")


if __name__ == "__main__":
    # 主执行流程
    genshin_data = fetch_genshin_data(DATA_URL)
    if genshin_data:
        create_dictionary_file(genshin_data)