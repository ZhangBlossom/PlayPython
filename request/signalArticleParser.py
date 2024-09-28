import os
import requests
from bs4 import BeautifulSoup
import re
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.lib.enums import TA_JUSTIFY
from io import BytesIO

# 注册中文字体
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

# 模拟浏览器的请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Referer': 'https://tech.meituan.com/'
}

# 创建一个Session对象
session = requests.Session()
session.proxies.update({'http': None, 'https': None})


def get_content(url):
    try:
        response = session.get(url, headers=headers, timeout=10)
        return response.content
    except Exception as e:
        print(f"无法获取网页内容。错误: {e}")
        return None


def download_image(img_url):
    try:
        response = session.get(img_url, headers=headers, timeout=10)
        if response.status_code == 200:
            return BytesIO(response.content)
        else:
            print(f"无法下载图片: {img_url}. 状态码: {response.status_code}")
            return None
    except Exception as e:
        print(f"下载图片时出错: {img_url}. 错误: {e}")
        return None


def scrape_meituan_tech_article(url):
    content = get_content(url)
    if not content:
        return None

    soup = BeautifulSoup(content, 'html.parser')

    title = soup.find('h1', class_='post-title').text.strip()

    meta_box = soup.find('div', class_='meta-box')
    date = meta_box.find('span', class_='m-post-date').text.strip()
    author = meta_box.find('span', class_='m-post-nick').text.replace('作者:', '').strip()

    content_div = soup.find('div', class_='post-content')
    content = []
    for element in content_div.find_all(['p', 'h2', 'h3', 'ul', 'ol', 'img']):
        if element.name in ['h2', 'h3']:
            content.append(('header', element.text.strip()))
        elif element.name == 'p':
            content.append(('paragraph', element.text.strip()))
        elif element.name in ['ul', 'ol']:
            list_items = [li.text.strip() for li in element.find_all('li')]
            content.append(('list', list_items))
        elif element.name == 'img':
            img_url = element.get('src')
            if img_url:
                content.append(('image', img_url))

    tags = [tag.text for tag in soup.find('span', class_='tag-links').find_all('a')]

    return {
        'title': title,
        'author': author,
        'date': date,
        'content': content,
        'tags': tags
    }


def create_pdf(article, output_filename):
    doc = SimpleDocTemplate(output_filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    styles = getSampleStyleSheet()

    # 为所有样式设置中文字体
    for style in styles.byName.values():
        style.fontName = 'STSong-Light'

    # 创建自定义样式
    styles.add(ParagraphStyle(name='ChineseTitle',
                              parent=styles['Title'],
                              fontName='STSong-Light',
                              fontSize=18,
                              alignment=TA_JUSTIFY))

    styles.add(ParagraphStyle(name='ChineseHeading2',
                              parent=styles['Heading2'],
                              fontName='STSong-Light',
                              fontSize=14,
                              alignment=TA_JUSTIFY))

    styles.add(ParagraphStyle(name='ChineseBody',
                              parent=styles['Normal'],
                              fontName='STSong-Light',
                              fontSize=10,
                              alignment=TA_JUSTIFY))

    story = []

    # 添加标题
    story.append(Paragraph(article['title'], styles['ChineseTitle']))
    story.append(Spacer(1, 12))

    # 添加作者和日期
    story.append(Paragraph(f"作者: {article['author']}", styles['ChineseBody']))
    story.append(Paragraph(f"日期: {article['date']}", styles['ChineseBody']))
    story.append(Spacer(1, 12))

    # 添加标签
    story.append(Paragraph(f"标签: {', '.join(article['tags'])}", styles['ChineseBody']))
    story.append(Spacer(1, 12))

    # 添加正文内容
    for item in article['content']:
        if item[0] == 'header':
            story.append(Paragraph(item[1], styles['ChineseHeading2']))
        elif item[0] == 'paragraph':
            story.append(Paragraph(item[1], styles['ChineseBody']))
        elif item[0] == 'list':
            for li in item[1]:
                story.append(Paragraph(f"• {li}", styles['ChineseBody']))
        elif item[0] == 'image':
            img_data = download_image(item[1])
            if img_data:
                img = Image(img_data, width=400, height=300)
                story.append(img)
        story.append(Spacer(1, 6))

    doc.build(story)

if __name__ == "__main__":
    url = 'https://tech.meituan.com/2023/12/29/the-evolution-of-terminals-from-standardization-to-digitalization.html'
    article = scrape_meituan_tech_article(url)

    if article:
        create_pdf(article, article.get('title') + '.pdf')
        print("PDF 文件已生成：" + article.get('title') + 'pdf')
    else:
        print("无法获取文章内容，PDF 生成失败。")