from utils.gpt4o import gpt4o
import re

class Agent:
    def __init__(self, prompt):
        self.prompt = prompt

    def infer(self, image, parse=True):
        text = gpt4o(self.prompt, image)
        return self.parser(text) if parse else text
    
    def parser(self, text):
        return text
    
class AgentSplit(Agent):
    def __init__(self):
        super().__init__("""你是一个擅长于搭建网页的网页工程师。
# CONTEXT #
我想实现一个将网页实现图片转换为实现该网页效果代码的项目。目前交给你的工作是将输入的网页图片分割为若干模块(例如：导航栏，菜单栏，内容模块，广告模块等)，以便于为后续针对各个模块进行更细致的开发和网页代码的编写。
# OBJECTIVE
将输入的网页图片分割为若干模块，以便于为后续针对各个模块进行更细致的开发和网页代码的编写。
# RESPONSE #
给出分割后的各模块的图片的坐标，图片左上角为原点，图片长宽分别记作1，给出模块左上角坐标(x1,y1)和右下角坐标(x2,y2)，最后输出模块名和(x1,y1,x2,y2), 保证x1<x2, y1<y2
# Initialize #
接下来的消息我会给你发送网页图片，收到后请按照以上规则输出分割后的各模块的名称以及坐标""")

    def parser(self, text):
        pattern = r"(\d+)\.\s+\*\*(.*?)\*\*\n\s+.*\((.*?)\)"
        matches = re.findall(pattern, text)

        # 解析坐标并存储为数组
        modules = []
        for match in matches:
            index, name, coords = match
            coords_list = [float(coord) for coord in coords.split(', ')]
            modules.append({'name': name, 'bbox': coords_list})

        return modules

class AgentI2C(Agent):
    def __init__(self):
        super().__init__("""你是一个擅长于搭建网页的网页工程师。
# CONTEXT #
我想实现一个将网页实现图片转换为实现该网页效果代码的项目。目前交给你的工作是根据分割后的网页模块的名称和图片，生成对应的HTML代码。
# OBJECTIVE
根据输入的网页图片和模块名称，生成模块HTML网页代码。
# RESPONSE #
给出能够实现模块功能的HTML网页代码。
# Initialize #
接下来的消息我会给你发送网页图片和模块名称，收到后请按照以上规则给出HTML代码""")

class AgentAssemble(Agent):
    def __init__(self):
        super().__init__("""# Role #
你是一个擅长于搭建网页的网页工程师。
# CONTEXT #
我想实现一个将网页实现图片转换为实现该网页效果代码的项目。目前交给你的工作是根据网页整体，划分后的模块名称，图片区域和对应的HTML代码，组合生成完整的网页HTML代码。
# OBJECTIVE
根据网页整体，划分后的模块名称，图片区域和对应的HTML代码，组合生成完整的网页HTML代码。
# RESPONSE #
给出能够实现整体功能的HTML网页代码。
# Initialize #
接下来的消息我会给你发送网页整体图片和模块名称，图片区域和对应的HTML代码，收到后请按照以上规则给出HTML代码""")        