import pandas as pd
data1 = pd.read_csv("data1.csv", encoding="gb2312")

keys = data1["地区"]
values = data1["薪资"]
geo = Geo("全国主要城市平均薪资", title_color="#fff", title_pos="left", width=1000, height=600, background_color='404a59')
geo.add("平均薪资", keys, values, visual_range=[3000, 20000], type='heatmap', label_text_color="#aaa",
        visual_text_color="#fff", symbol_size=15, is_visualmap=True, is_roam=True, label_pos="inside")
geo.render(path="全国主要城市平均薪资1.html")
