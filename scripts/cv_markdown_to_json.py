#!/usr/bin/env python3
"""
将 Markdown 简历转换为 JSON 格式的脚本
Author: Yuan Chen
"""

import os
import re
import json
import yaml
import argparse
from datetime import datetime, date
from pathlib import Path
import glob

# 处理日期对象的自定义 JSON 编码器
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

def parse_markdown_cv(md_file):
    """解析 Markdown 简历并提取章节。"""
    with open(md_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 去除 YAML 头部信息
    content = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)
    
    # 提取章节内容
    sections = {}
    current_section = None
    section_content = []
    
    for line in content.split('\n'):
        if re.match(r'^=+$', line):
            continue
        
        section_match = re.match(r'^([A-Za-z\s]+)$', line.strip())
        if section_match and len(line.strip()) > 0:
            if current_section:
                sections[current_section] = '\n'.join(section_content).strip()
                section_content = []
            current_section = section_match.group(1).strip()
        elif current_section:
            section_content.append(line)
    
    # 补上最后一个章节
    if current_section and section_content:
        sections[current_section] = '\n'.join(section_content).strip()
    
    return sections

def parse_config(config_file):
    """解析 Jekyll _config.yml 并读取附加信息。"""
    if not os.path.exists(config_file):
        return {}
    
    with open(config_file, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    
    return config

def extract_author_info(config):
    """从配置文件中提取作者信息。"""
    author_info = {
        "name": config.get('name', ''),
        "email": "",
        "phone": "",
        "website": config.get('url', ''),
        "summary": "",
        "location": {
            "address": "",
            "postalCode": "",
            "city": "",
            "countryCode": "US",
            "region": ""
        },
        "profiles": []
    }
    
    # 若存在 author 字段，则提取详细信息
    if 'author' in config:
        author = config.get('author', {})
        
        # 若 author.name 存在，则覆盖默认 name
        if author.get('name'):
            author_info['name'] = author.get('name')
        
        # 添加邮箱
        if author.get('email'):
            author_info['email'] = author.get('email')
        
        # 添加地点
        if author.get('location'):
            author_info['location']['city'] = author.get('location', '')
        
        # 将雇主信息写入摘要
        if author.get('employer'):
            author_info['summary'] = f"Currently employed at {author.get('employer')}"
        
        # 若有 bio，则补充到摘要中
        if author.get('bio'):
            if author_info['summary']:
                author_info['summary'] += f". {author.get('bio')}"
            else:
                author_info['summary'] = author.get('bio')
        
        # 组装社交档案
        profiles = []
        
        # 学术平台档案
        if author.get('googlescholar'):
            profiles.append({
                "network": "Google Scholar",
                "username": "",
                "url": author.get('googlescholar')
            })
        
        if author.get('orcid'):
            profiles.append({
                "network": "ORCID",
                "username": "",
                "url": author.get('orcid')
            })
        
        if author.get('researchgate'):
            profiles.append({
                "network": "ResearchGate",
                "username": "",
                "url": author.get('researchgate')
            })
        
        # 社交媒体档案
        if author.get('github'):
            profiles.append({
                "network": "GitHub",
                "username": author.get('github'),
                "url": f"https://github.com/{author.get('github')}"
            })
        
        if author.get('linkedin'):
            profiles.append({
                "network": "LinkedIn",
                "username": author.get('linkedin'),
                "url": f"https://www.linkedin.com/in/{author.get('linkedin')}"
            })
        
        if author.get('twitter'):
            profiles.append({
                "network": "Twitter",
                "username": author.get('twitter'),
                "url": f"https://twitter.com/{author.get('twitter')}"
            })
        
        author_info['profiles'] = profiles
    
    return author_info

def parse_education(education_text):
    """解析教育经历章节。"""
    education_entries = []
    
    # 提取教育经历条目
    entries = re.findall(r'\* (.*?)(?=\n\*|\Z)', education_text, re.DOTALL)
    
    for entry in entries:
        # 解析学位、学校与年份
        match = re.match(r'([^,]+), ([^,]+), (\d{4})(.*)', entry.strip())
        if match:
            degree, institution, year, additional = match.groups()
            
            # 若存在 GPA 则提取
            gpa_match = re.search(r'GPA: ([\d\.]+)', additional)
            gpa = gpa_match.group(1) if gpa_match else None
            
            education_entries.append({
                "institution": institution.strip(),
                "area": degree.strip(),
                "studyType": "",
                "startDate": "",
                "endDate": year.strip(),
                "gpa": gpa,
                "courses": []
            })
    
    return education_entries

def parse_work_experience(work_text):
    """解析工作经历章节。"""
    work_entries = []
    
    # 提取工作经历条目
    entries = re.findall(r'\* (.*?)(?=\n\*|\Z)', work_text, re.DOTALL)
    
    for entry in entries:
        lines = entry.strip().split('\n')
        if not lines:
            continue
            
        # 解析职位与单位
        first_line = lines[0].strip()
        position_match = re.match(r'(.*?), (.*?)(?:, |$)', first_line)
        
        if position_match:
            position, company = position_match.groups()
            
            # 提取起止时间（若存在）
            date_match = re.search(r'(\d{4})\s*-\s*(\d{4}|present)', entry, re.IGNORECASE)
            start_date = date_match.group(1) if date_match else ""
            end_date = date_match.group(2) if date_match else ""
            
            # 提取亮点/职责条目
            highlights = []
            for line in lines[1:]:
                if line.strip().startswith('*') or line.strip().startswith('-'):
                    highlights.append(line.strip()[1:].strip())
            
            work_entries.append({
                "company": company.strip(),
                "position": position.strip(),
                "website": "",
                "startDate": start_date,
                "endDate": end_date,
                "summary": "",
                "highlights": highlights
            })
    
    return work_entries

def parse_skills(skills_text):
    """解析技能章节。"""
    skills_entries = []
    
    # 提取技能分类
    categories = re.findall(r'(?:^|\n)(\w+.*?):\s*(.*?)(?=\n\w+.*?:|\Z)', skills_text, re.DOTALL)
    
    for category, skills in categories:
        # 提取具体技能项
        skill_list = [s.strip() for s in re.split(r',|\n', skills) if s.strip()]
        
        skills_entries.append({
            "name": category.strip(),
            "level": "",
            "keywords": skill_list
        })
    
    return skills_entries

def parse_publications(pub_dir):
    """从 _publications 目录解析出版物。"""
    publications = []
    
    if not os.path.exists(pub_dir):
        return publications
    
    for pub_file in sorted(glob.glob(os.path.join(pub_dir, "*.md"))):
        with open(pub_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 提取 front matter
        front_matter_match = re.match(r'^---\s*(.*?)\s*---', content, re.DOTALL)
        if front_matter_match:
            front_matter = yaml.safe_load(front_matter_match.group(1))
            
            # 提取出版物详情
            pub_entry = {
                "name": front_matter.get('title', ''),
                "publisher": front_matter.get('venue', ''),
                "releaseDate": front_matter.get('date', ''),
                "website": front_matter.get('paperurl', ''),
                "summary": front_matter.get('excerpt', '')
            }
            
            publications.append(pub_entry)
    
    return publications

def parse_talks(talks_dir):
    """从 _talks 目录解析演讲信息。"""
    talks = []
    
    if not os.path.exists(talks_dir):
        return talks
    
    for talk_file in sorted(glob.glob(os.path.join(talks_dir, "*.md"))):
        with open(talk_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 提取 front matter
        front_matter_match = re.match(r'^---\s*(.*?)\s*---', content, re.DOTALL)
        if front_matter_match:
            front_matter = yaml.safe_load(front_matter_match.group(1))
            
            # 提取演讲详情
            talk_entry = {
                "name": front_matter.get('title', ''),
                "event": front_matter.get('venue', ''),
                "date": front_matter.get('date', ''),
                "location": front_matter.get('location', ''),
                "description": front_matter.get('excerpt', '')
            }
            
            talks.append(talk_entry)
    
    return talks

def parse_teaching(teaching_dir):
    """从 _teaching 目录解析教学信息。"""
    teaching = []
    
    if not os.path.exists(teaching_dir):
        return teaching
    
    for teaching_file in sorted(glob.glob(os.path.join(teaching_dir, "*.md"))):
        with open(teaching_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 提取 front matter
        front_matter_match = re.match(r'^---\s*(.*?)\s*---', content, re.DOTALL)
        if front_matter_match:
            front_matter = yaml.safe_load(front_matter_match.group(1))
            
            # 提取教学详情
            teaching_entry = {
                "course": front_matter.get('title', ''),
                "institution": front_matter.get('venue', ''),
                "date": front_matter.get('date', ''),
                "role": front_matter.get('type', ''),
                "description": front_matter.get('excerpt', '')
            }
            
            teaching.append(teaching_entry)
    
    return teaching

def parse_portfolio(portfolio_dir):
    """从 _portfolio 目录解析项目条目。"""
    portfolio = []
    
    if not os.path.exists(portfolio_dir):
        return portfolio
    
    for portfolio_file in sorted(glob.glob(os.path.join(portfolio_dir, "*.md"))):
        with open(portfolio_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 提取 front matter
        front_matter_match = re.match(r'^---\s*(.*?)\s*---', content, re.DOTALL)
        if front_matter_match:
            front_matter = yaml.safe_load(front_matter_match.group(1))
            
            # 提取项目详情
            portfolio_entry = {
                "name": front_matter.get('title', ''),
                "category": front_matter.get('collection', 'portfolio'),
                "date": front_matter.get('date', ''),
                "url": front_matter.get('permalink', ''),
                "description": front_matter.get('excerpt', '')
            }
            
            portfolio.append(portfolio_entry)
    
    return portfolio

def create_cv_json(md_file, config_file, repo_root, output_file):
    """基于 Markdown 与仓库数据生成 JSON 简历。"""
    # 解析 Markdown 简历
    sections = parse_markdown_cv(md_file)
    
    # 解析配置文件
    config = parse_config(config_file)
    
    # 提取作者信息
    author_info = extract_author_info(config)
    
    # 组装 JSON 结构
    cv_json = {
        "basics": author_info,
        "work": parse_work_experience(sections.get('Work experience', '')),
        "education": parse_education(sections.get('Education', '')),
        "skills": parse_skills(sections.get('Skills', '')),
        "languages": [],
        "interests": [],
        "references": []
    }
    
    # 填充出版物
    cv_json["publications"] = parse_publications(os.path.join(repo_root, "_publications"))
    
    # 填充演讲
    cv_json["presentations"] = parse_talks(os.path.join(repo_root, "_talks"))
    
    # 填充教学经历
    cv_json["teaching"] = parse_teaching(os.path.join(repo_root, "_teaching"))
    
    # 填充项目条目
    cv_json["portfolio"] = parse_portfolio(os.path.join(repo_root, "_portfolio"))
    
    # 若配置中存在语言/兴趣字段，则一并填充
    if 'languages' in config:
        cv_json["languages"] = config.get('languages', [])
    
    if 'interests' in config:
        cv_json["interests"] = config.get('interests', [])
    
    # 将 JSON 写入文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(cv_json, file, indent=2, cls=DateTimeEncoder)
    
    print(f"Successfully converted {md_file} to {output_file}")

def main():
    """主函数：解析参数并执行转换。"""
    parser = argparse.ArgumentParser(description='Convert markdown CV to JSON format')
    parser.add_argument('--input', '-i', required=True, help='Input markdown CV file')
    parser.add_argument('--output', '-o', required=True, help='Output JSON file')
    parser.add_argument('--config', '-c', help='Jekyll _config.yml file')
    
    args = parser.parse_args()
    
    # 获取仓库根目录（输入文件目录的上一级）
    repo_root = str(Path(args.input).parent.parent)
    
    create_cv_json(args.input, args.config, repo_root, args.output)

if __name__ == '__main__':
    main()
