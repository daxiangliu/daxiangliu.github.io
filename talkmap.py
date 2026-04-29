# 使用 Leaflet 生成演讲地点聚类地图
#
# 请在包含演讲 Markdown 文件的仓库根目录运行此脚本（会读取 _talks/*.md）。
# 脚本会提取每个文件中的 location 字段，通过 geopy/Nominatim 做地理编码，
# 再用 getorg 生成独立的聚类地图数据、HTML 与 JavaScript。功能上等同于
# #talkmap Jupyter notebook.
import frontmatter
import glob
import getorg
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut

# 默认超时时间（秒）
TIMEOUT = 5

# 收集 Markdown 文件
g = glob.glob("_talks/*.md")

# 初始化地理编码器
geocoder = Nominatim(user_agent="academicpages.github.io")
location_dict = {}
location = ""
permalink = ""
title = ""

# 执行地理编码
for file in g:
    # 读取文件
    data = frontmatter.load(file)
    data = data.to_dict()

    # 若无 location 字段则跳过
    if 'location' not in data:
        continue

    # 组织描述信息
    title = data['title'].strip()
    venue = data['venue'].strip()
    location = data['location'].strip()
    description = f"{title}<br />{venue}; {location}"

    # 对地点进行编码并输出状态
    try:
        location_dict[description] = geocoder.geocode(location, timeout=TIMEOUT)
        print(description, location_dict[description])
    except ValueError as ex:
        print(f"Error: geocode failed on input {location} with message {ex}")
    except GeocoderTimedOut as ex:
        print(f"Error: geocode timed out on input {location} with message {ex}")
    except Exception as ex:
        print(f"An unhandled exception occurred while processing input {location} with message {ex}")

# 输出地图文件
m = getorg.orgmap.create_map_obj()
getorg.orgmap.output_html_cluster_map(location_dict, folder_name="talkmap", hashed_usernames=False)
