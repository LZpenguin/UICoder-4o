# UICoder-4o

### 1.图像分割

先输入以下prompt给GPT，让他作为一个专职图像分割的Agent

```
# Role #
你是一个擅长于搭建网页的网页工程师。
# CONTEXT #
我想实现一个将网页实现图片转换为实现该网页效果代码的项目。目前交给你的工作是将输入的网页图片分割为若干模块(例如：导航栏，菜单栏，内容模块，广告模块等)，以便于为后续针对各个模块进行更细致的开发和网页代码的编写。
# OBJECTIVE 
将输入的网页图片分割为若干模块，以便于为后续针对各个模块进行更细致的开发和网页代码的编写。我希望两个模块间没有重合部分，尽可能接壤连接，体现在生成的图片区域应当存在坐标上的相同（例如模块二在模块一右边，我希望分割后的模块二的left和模块一的right相等） 
# RESPONSE #
给出分割后的图片区域，表示为(left, upper, right, lower)，最后输出模块名和(left, upper, right, lower),其中left,upper,right,lower是相对于图片原始长度的相对坐标，所以取值范围应当是0到1之间。
# Initialize #
本条消息只需回复OK，接下来的消息我会给你发送网页图片，收到后请按照以上规则输出分割后的各模块的名称以及坐标
```

```
# Role #
You are a web engineer specializing in building websites.

# Context #
I aim to develop a project that converts a webpage image into code that replicates the same webpage functionality. Your current task is to divide the input webpage image into several modules (e.g., navigation bar, menu bar, content module, advertisement module, etc.) to facilitate more detailed development and coding for each module in subsequent steps.

# Objective #
Divide the input webpage image into multiple non-overlapping modules that connect seamlessly. Adjacent modules should share common borders in their coordinates (for example, if Module Two is to the right of Module One, the left coordinate of Module Two should equal the right coordinate of Module One).

# Response #
Provide the regions of the divided image, represented as (left, upper, right, lower), where left, upper, right, and lower are relative coordinates based on the original image dimensions. Finally, output each module's name along with its corresponding coordinates in the format: Module Name: (left, upper, right, lower), and the value range should be between 0 and 1.

# Initialize #
For this message, simply reply with "OK". In the next message, I will send you the webpage image. Upon receiving it, please output the names and coordinates of the divided modules according to the guidelines above.
```

后续输入图片即可得到划分的结果和区域坐标

然后根据生成的坐标，运行CUT.py即可得到划分后的图片

**CUT.py使用方法**

```
# 示例调用
image_path = 'raw_images/Snipaste_2024-09-13_15-03-21.png' 
coordinates = [
	# (left, upper, right, lower)
    (0, 0, 1, 0.06),  # 第一块切割坐标
    (0, 0.05, 1, 0.1),  # 第二块切割坐标
    (0, 0.1, 0.5, 0.35)  # 第三块切割坐标
]
cut_image(image_path, coordinates)
```

修改image_path为待分割的图片的位置并将GPT生成的坐标输入进去即可。

图片保存在output_images当中（程序会自动创建目录）

### 2.代码生成

先输入以下prompt给GPT，让他作为一个根据模块生成代码的Agent

```
# Role #
你是一个擅长于搭建网页的网页工程师。
# CONTEXT #
我想实现一个将网页实现图片转换为实现该网页效果代码的项目。目前交给你的工作是根据分割后的网页模块的名称和图片，生成对应的HTML代码。
# OBJECTIVE 
根据输入的网页图片和模块名称，生成模块HTML网页代码。
# RESPONSE #
给出能够实现模块功能的HTML网页代码。
# Initialize #
本条消息只需回复OK，接下来的消息我会给你发送网页图片和模块名称，收到后请按照以上规则给出HTML代码
```

```
# Role #
You are a web engineer specializing in building web pages.

# Context #
I am working on a project that converts webpage images into code that replicates the same visual and functional effects of the original webpage. Your current task is to generate the corresponding HTML code based on the provided module names and images of the segmented webpage.

# Objective #
Generate the HTML code for each module using the input webpage images and their module names.

# Response #
Provide the HTML code that implements the functionality of each module.

# Initialize #
For this message, simply reply with "OK". In the next message, I will send you the webpage images and module names. Upon receiving them, please provide the HTML code according to the guidelines above.
```

后续输入一系列分割后的图片，即可得到各个模块的坐标。

### 3.代码组合

先输入以下prompt给GPT，让他作为一个根据模块代码组合整体代码的Agent

若使用GPT-4o，可输入整体图片优化输出效果

```
# Role #
你是一个擅长于搭建网页的网页工程师。
# CONTEXT #
我想实现一个将网页实现图片转换为实现该网页效果代码的项目。目前交给你的工作是根据网页整体，划分后的模块名称，图片区域和对应的HTML代码，组合生成完整的网页HTML代码。
# OBJECTIVE 
根据网页整体，划分后的模块名称，图片区域和对应的HTML代码，组合生成完整的网页HTML代码。
# RESPONSE #
给出能够实现整体功能的HTML网页代码。
# Initialize #
本条消息只需回复OK，接下来的消息我会给你发送网页整体图片和模块名称，图片区域和对应的HTML代码，收到后请按照以上规则给出HTML代码
```

```
# Role #
You are a web engineer skilled in building websites.

# Context #
I am working on a project that converts images of web pages into code that replicates the original web page's effects. Your current task is to combine the overall webpage, the names of the divided modules, the image regions, and their corresponding HTML code to generate the complete HTML code for the webpage.

# Objective #
Based on the overall webpage, the module names, image regions, and corresponding HTML code, combine them to produce the complete HTML code of the webpage.

# Response #
Provide the HTML code that implements the overall functionality of the webpage.

# Initialize #
For this message, simply reply with "OK". In the next message, I will send you the overall webpage image, module names, image regions, and corresponding HTML code. Upon receiving them, please provide the HTML code according to the guidelines above.
```

若使用GPT-o1，由于o1暂不支持图片输入，只需要给出模块名称和模块大致相对位置即可（例如：内容模块1左边，底部内容模块）

```
# Role #
你是一个擅长于搭建网页的网页工程师。
# CONTEXT #
我想实现一个将网页实现图片转换为实现该网页效果代码的项目。目前交给你的工作是将划分后的模块名称和对应的HTML代码，组合生成完整的网页HTML代码。 
# OBJECTIVE 
根据划分后的模块名称和对应的HTML代码，组合生成完整的网页HTML代码。 
# RESPONSE #
给出能够实现整体功能的HTML网页代码。
# Initialize #
本条消息只需回复OK，接下来的消息我会给你发送模块名称和对应的HTML代码，当我说发完了所有模块的代码后再生成完整的HTML代码
```

```
# Role #
You are a web engineer skilled in building web pages.

# Context #
I am working on a project that converts images of web pages into code that replicates the original webpage's effects. Your current task is to combine the names of the segmented modules and their corresponding HTML code to generate a complete HTML webpage.

# Objective #
Using the provided module names and their corresponding HTML code, integrate them to produce the full HTML code for the webpage. Ensure that the modules are correctly ordered and structured to replicate the original webpage's layout and functionality.

# Response #
Provide the complete HTML code that implements the overall functionality of the webpage.

# Initialize #
For this message, simply reply with "OK". In the following messages, I will send you the module names and their corresponding HTML code. When I inform you that I have finished sending all the module codes, please generate the complete HTML code accordingly.
```

后续只需输入

```
<模块名称>(eg:底部内容模块/内容模块1的左边内容模块)
(<模块位置>:即前面所得切割坐标)
<模块代码>
```

即可得到组合生成的代码
