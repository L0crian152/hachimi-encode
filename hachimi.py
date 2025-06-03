#!/usr/bin/env python3
import sys
import argparse

# 4位编码词典（按词长倒序排列）
CODE_MAP = {
    '0000': '叮咚鸡',    
    '0001': '西苦',
    '0010': '录多',
    '0011': '牛魔',
    '0100': '纳录',
    '0101': '哈基米',    
    '0110': '悠答',
    '0111': '马集里',
    '1000': '哈呀哭',
    '1001': '米基',
    '1010': '曼波',
    '1011': '阿西',
    '1100': '多',
    '1101': '哦',
    '1110': '噶',
    '1111': '哈！'      
}

# 自动生成解码词典（按词长降序）
DECODE_MAP = {v: k for k, v in sorted(CODE_MAP.items(), 
                                     key=lambda x: (-len(x[1]), x[1]))}

def encode(text):
    """编码为哈基米语"""
    byte_data = text.encode('utf-8')
    binary = ''.join(f"{byte:08b}" for byte in byte_data)
    
    # 填充至4的倍数
    padding = (4 - len(binary) % 4) % 4
    binary += '0' * padding
    
    return ''.join(CODE_MAP[binary[i:i+4]] for i in range(0, len(binary),4))

def decode(hachimicode):
    """解码哈基米语"""
    binary = []
    remaining = hachimicode.strip()
    
    # 动态最长匹配
    while remaining:
        for word in DECODE_MAP:
            if remaining.startswith(word):
                binary.append(DECODE_MAP[word])
                remaining = remaining[len(word):]
                break
        else:
            raise ValueError(f"无效编码: '{remaining[:10]}...'")
    
    binary_str = ''.join(binary)
    # 计算实际有效位
    original_bits = len(binary_str) - (len(binary_str) % 8)
    byte_str = binary_str[:original_bits]
    
    try:
        return bytes(int(byte_str[i:i+8],2) for i in range(0,len(byte_str),8)
             ).decode('utf-8')
    except UnicodeDecodeError:
        return bytes.fromhex(f"{int(byte_str,2):x}").decode('utf-8','replace')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='哈基米语编解码器V2')
    parser.add_argument('mode', choices=['encode','decode'], 
                       help='操作模式')
    parser.add_argument('text', nargs='?', help='输入内容')
    
    args = parser.parse_args()
    input_text = args.text or sys.stdin.read().strip()
    
    try:
        if args.mode == 'encode':
            print(encode(input_text))
        else:
            print(decode(input_text))
    except Exception as e:
        sys.stderr.write(f"错误: {str(e)}\n")
        sys.exit(1)
