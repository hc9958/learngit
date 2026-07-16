from transformers import AutoModelForCausalLM, AutoTokenizer
# 安装依赖命令(已在pytorch_env环境直接跳过)：
# pip install transformers accelerate sentencepiece safetensors

# ========== 这里是你电脑真实模型路径 ==========
model_name = r"C:\Users\hp\Qwen2.5-1.5B-Instruct"

# 加载模型，自动使用GPU加速
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",  # 自动分配GPU显存
    trust_remote_code=True
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 定义Prompt模板：文本情感分类
prompt_template = "请判断以下文本属于哪个类别：{text}。可选类别有：正面、负面、中立。"

# 输入用户评价
input_text = input("请输入电影评价：")
prompt_input = prompt_template.format(text=input_text)
print('prompt_input:', prompt_input)

# 分词编码，自动放到GPU
inputs = tokenizer(prompt_input, return_tensors="pt").to("cuda")
print("inputs:", inputs)

# 模型推理生成结果
output_sequences = model.generate(
    inputs.input_ids,
    attention_mask=inputs.attention_mask,
    max_new_tokens=512
)
print("output_sequences:", output_sequences)

# 解码输出文本
generated_text = tokenizer.decode(output_sequences[0], skip_special_tokens=True)
print("完整输出文本：", generated_text)

# 只打印模型新生成的回答（剔除输入prompt）
text = generated_text[len(prompt_input):]
print("模型分类结果：", text)