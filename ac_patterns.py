#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
@Brief: AC多模式匹配实现算法
@Date: 2014/03/30
'''


import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ACMatch(object):
    def __init__(self,pattern_file):
        #多个pattern组成的list
        self.patterns = []
        #状态转移
        self.goto = {}
        #失败转移
        self.failure = {}
        #匹配输出
        self.output = {}
        with open(pattern_file, 'r') as f:
            for line in f:
                line = line.strip().strip("\"")
                self.patterns.append(line)

        self.__construct_goto(self.patterns)
        self.__construct_failure()
    
    def __del__(self):
        self.patterns= None
        self.goto = None
        self.failure = None
        self.output = None

    def __construct_goto(self, patterns):
        '''
        @Brief: 构造状态转移数据结构和匹配输出中间状态
        @patterns:多个pattern组成的list
        '''
        
        #全局唯一状态编号
        global_state = 1
        #遍历每一个pattern
        for item in patterns:
            #从状态0开始
            new_state = 0
            #从pattern的第一个字符开始
            index = 0
            #复用前面已经构造好的前缀字符串
            while new_state in self.goto and index < len(item) and \
                  item[index] in self.goto[new_state]:
                new_state = self.goto[new_state][item[index]]
                index = index + 1
            for i in range(index,len(item)):
                self.goto.setdefault(new_state, {})
                self.goto[new_state][item[i]] = global_state
                new_state = global_state
                global_state = global_state + 1
             
            #构造匹配输出的中间状态
            self.output.setdefault(new_state, [])
            self.output[new_state].append(item)

    def __construct_failure(self):
        '''
        @Brief: 构造失败转移数据结构和匹配输出最终结构
        '''

        #图的宽度优先遍历
        queue_list = []
        
        #初始化深度为1的结点
        for key in self.goto[0]:
            state_depth_1 = self.goto[0][key]
            self.failure[state_depth_1] = 0
            queue_list.append(state_depth_1)

        #宽度优先遍历
        while len(queue_list) > 0:
            #queue pop
            state = queue_list[0]
            queue_list = queue_list[1:]
            if state in self.goto:
                for key in self.goto[state]:
                    state_depth_n = self.goto[state][key]
                    queue_list.append(state_depth_n)
                    temp_state = self.failure[state]
                    while (temp_state not in self.goto or key not in self.goto[temp_state]) \
                           and temp_state != 0:
                        temp_state = self.failure[temp_state]
                    #找到公共前缀
                    if temp_state in self.goto and key in self.goto[temp_state]:
                        self.failure[state_depth_n] = self.goto[temp_state][key]
                    else:
                        self.failure[state_depth_n] = 0
                    
                    if self.failure[state_depth_n] in self.output:
                        self.output.setdefault(state_depth_n, [])
                        self.output[state_depth_n].extend(self.output[self.failure[state_depth_n]])

    def patterns_match(self, text):
        '''
        @Brief: 多模式匹配过程
        @text:需要匹配的文本
        '''
        retval = [] 
        #当前的状态编号
        state = 0
        #遍历文本的每一个字符
        for item in text:
            #如果正常转移不下去，就进行失败转移过程
            while (state not in self.goto or item not in self.goto[state]) \
                   and state != 0:
                state = self.failure[state]
            
            #进行正常转移
            if state in self.goto and item in self.goto[state]:
                state = self.goto[state][item]
            else:
                state = 0

            #如果可以输出了，就马上输出
            if state in self.output:
                for output in self.output[state]:
                    retval.append(output)
        return retval
    

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write('注意：需要传入一个词包文件和文本！\n')
        sys.exit(0)
    match = ACMatch(sys.argv[1])
    f2=open(sys.argv[2],'r')
    line=f2.readline()
    print match.patterns_match(line.strip())
