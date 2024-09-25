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
        super().__init__("""# Role #
You are a web engineer specializing in building websites.
# Context #
I aim to develop a project that converts a webpage image into code that replicates the same webpage functionality. Your current task is to divide the input webpage image into several modules (e.g., navigation bar, menu bar, content module, advertisement module, etc.) to facilitate more detailed development and coding for each module in subsequent steps.
# Objective #
Divide the input webpage image into multiple non-overlapping modules that connect seamlessly. Adjacent modules should share common borders in their coordinates (for example, if Module Two is to the right of Module One, the left coordinate of Module Two should equal the right coordinate of Module One).
# Response #
Provide the regions of the divided image, represented as (left, upper, right, lower), where left, upper, right, and lower are relative coordinates based on the original image dimensions. Finally, output each module's name along with its corresponding coordinates in the format: Module Name: (left, upper, right, lower), and the value range should be between 0 and 1.
# Initialize #
For this message, simply reply with "OK". In the next message, I will send you the webpage image. Upon receiving it, please output the names and coordinates of the divided modules according to the guidelines above.""")

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
        super().__init__("""# Role #
You are a web engineer specializing in building web pages.
# Context #
I am working on a project that converts webpage images into code that replicates the same visual and functional effects of the original webpage. Your current task is to generate the corresponding HTML code based on the provided module names and images of the segmented webpage.
# Objective #
Generate the HTML code for each module using the input webpage images and their module names.
# Response #
Provide the HTML code that implements the functionality of each module.
# Initialize #
For this message, simply reply with "OK". In the next message, I will send you the webpage images and module names. Upon receiving them, please provide the HTML code according to the guidelines above.""")


class AgentAssemble(Agent):
    def __init__(self):
        super().__init__("""# Role #
You are a web engineer skilled in building websites.
# Context #
I am working on a project that converts images of web pages into code that replicates the original web page's effects. Your current task is to combine the overall webpage, the names of the divided modules, the image regions, and their corresponding HTML code to generate the complete HTML code for the webpage.
# Objective #
Based on the overall webpage, the module names, image regions, and corresponding HTML code, combine them to produce the complete HTML code of the webpage.
# Response #
Provide the HTML code that implements the overall functionality of the webpage.
# Initialize #
For this message, simply reply with "OK". In the next message, I will send you the overall webpage image, module names, image regions, and corresponding HTML code. Upon receiving them, please provide the HTML code according to the guidelines above.""")
