# encoding: utf-8
__author__ = 'fanzhikang'
__date__ = '2018/10/17 22:20'
import requests
import json
import pandas as pd
import xlwt



class Crawl:
    base_url = 'https://www.kaoshixing.com/account/login'
    login_data = {
        'userName': 'CECC511@cecctm.com',
        'userNameInput': 'CECC511',
        'newCompanyId': 5769,
        'password': '5c3a0d081b1bf8b462429e45f1c7d579',
        'remember': True
    }
    headers_base = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    test_url = 'https://admin.kaoshixing.com/admin/showtestqm_grid/'
    data = 'current=1&rowCount=1435&searchPhrase=&status=&testType=&commitIds=&testDifficult=&testCreater=&testClassification=&testStartTime=&testEndTime=&fullText=&checkDup=0'


    def __init__(self):
        self.dict1 = {}
        self.dict2 = {}
        self.dict3 = {}
        self.dict4 = {}
        self.dict5 = {}
        self.list1 = []
        self.list2 = []
        self.list3 = []
        self.list4 = []
        self.list5 = []
        self.detail_url = 'https://admin.kaoshixing.com/admin/load_data?&id='
        self.session = requests.session()

    def login(self):
        self.session.post(self.base_url, headers=self.headers_base, data = self.login_data)

    def get_datas(self):
        self.login()
        content = self.session.post('https://admin.kaoshixing.com/admin/showtestqm_grid/', headers=self.headers_base, data= self.data)
        content = content.content.decode(encoding='utf-8')
        content_dict = json.loads(content)
        for li in content_dict['bizContent']['rows']:
            if li['type'] == '问答':
                dict = {}
                question = li['content']
                # self.list1.append(question)
                dif = li['difficult']
                classification = li['classification'].split('/')[-1]
                id = li['id']
                url = self.detail_url + id
                answer = self.parse_1(url)
                dict['question'] = question
                dict['answer'] = answer
                dict['classification'] = classification
                dict['dif'] = dif
                self.list1.append(dict)
                # self.list2.append(answer)
                # self.list3.append(classification)
                # self.list4.append(dif)
            elif li['type'] == '填空':
                dict = {}
                question = li['content']
                dif = li['difficult']
                classification = li['classification'].split('/')[-1]
                id = li['id']
                url = self.detail_url + id
                answers = self.parse_2(url)
                dict['question'] = question
                dict['answer1'] = answers[0]
                dict['answer2'] = answers[1]
                dict['answer3'] = answers[2]
                dict['answer4'] = answers[3]
                dict['classification'] = classification
                dict['dif'] = dif
                self.list2.append(dict)
            elif li['type'] == '判断':
                dict = {}
                question = li['content']
                dif = li['difficult']
                classification = li['classification'].split('/')[-1]
                id = li['id']
                url = self.detail_url + id
                answer = self.parse_3(url)
                dict['question'] = question
                dict['answer'] = answer
                dict['classification'] = classification
                dict['dif'] = dif
                self.list3.append(dict)
            elif li['type'] == '多选':
                dict = {}
                question = li['content']
                dif = li['difficult']
                classification = li['classification'].split('/')[-1]
                id = li['id']
                url = self.detail_url + id
                choices, answer, analysis = self.parse_4(url)
                dict['question'] = question
                dict['choice1'] = choices[0]
                dict['choice2'] = choices[1]
                dict['choice3'] = choices[2]
                dict['choice4'] = choices[3]
                dict['answer'] = answer
                dict['analysis'] = analysis
                dict['classification'] = classification
                dict['dif'] = dif
                self.list4.append(dict)
            elif li['type'] == '单选':
                dict = {}
                question = li['content']
                dif = li['difficult']
                classification = li['classification'].split('/')[-1]
                id = li['id']
                url = self.detail_url + id
                choices, answer, analysis = self.parse_4(url)
                dict['question'] = question
                dict['choice1'] = choices[0]
                dict['choice2'] = choices[1]
                dict['choice3'] = choices[2]
                dict['choice4'] = choices[3]
                dict['answer'] = answer
                dict['analysis'] = analysis
                dict['classification'] = classification
                dict['dif'] = dif
                self.list5.append(dict)



    def parse_1(self,url):
        data_content = self.session.get(url)
        data_content = data_content.content.decode(encoding='utf-8')
        data_dict = json.loads(data_content)
        answer = data_dict['bizContent']['answer1']
        return answer

    def parse_2(self, url):
        answers = []
        data_content = self.session.get(url)
        data_content = data_content.content.decode(encoding='utf-8')
        data_dict = json.loads(data_content)
        answers.append(data_dict['bizContent'].get('answer1', ''))
        answers.append(data_dict['bizContent'].get('answer2', ''))
        answers.append(data_dict['bizContent'].get('answer3', ''))
        answers.append(data_dict['bizContent'].get('answer4', ''))
        return answers

    def parse_3(self,url):
        data_content = self.session.get(url)
        data_content = data_content.content.decode(encoding='utf-8')
        data_dict = json.loads(data_content)
        if data_dict['bizContent'].get('key1','') == '1':
            answer = '正确'
        else:
            answer = '错误'
        return answer

    def parse_4(self, url):
        choices = []
        data_content = self.session.get(url)
        data_content = data_content.content.decode(encoding='utf-8')
        data_dict = json.loads(data_content)
        choices.append(data_dict['bizContent'].get('answer1', ''))
        choices.append(data_dict['bizContent'].get('answer2', ''))
        choices.append(data_dict['bizContent'].get('answer3', ''))
        choices.append(data_dict['bizContent'].get('answer4', ''))
        answer = data_dict['bizContent'].get('test_ans_right', '')
        analysis = data_dict['bizContent'].get('analysis', '')
        return choices, answer, analysis


    def save_sheet(self):
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet1 = workbook.add_sheet('问答')
        sheet2 = workbook.add_sheet('填空')
        sheet3 = workbook.add_sheet('判断')
        sheet4 = workbook.add_sheet('多选')
        sheet5 = workbook.add_sheet('单选')
        head1 = ['题干', '答案', '分类', '难度']
        head2 = ['题干', '答案1', '答案2', '答案3', '答案4', '分类', '难度']
        head3 = ['题干', '答案', '分类', '难度']
        head4 = ['题干', '选项A', '选项B', '选项C', '选项D', '答案', '解析', '分类', '难度']
        head5 = ['题干', '选项A', '选项B', '选项C', '选项D', '答案', '解析', '分类', '难度']

        for h in range(len(head1)):
            sheet1.write(0, h, head1[h])
        i = 1
        for li in demo.list1:
            sheet1.write(i, 0, li['question'])
            sheet1.write(i, 1, li['answer'])
            sheet1.write(i, 2, li['classification'])
            sheet1.write(i, 3, li['dif'])
            i += 1

        for h in range(len(head2)):
            sheet2.write(0, h, head2[h])
        i = 1
        for li in demo.list2:
            sheet2.write(i, 0, li['question'])
            sheet2.write(i, 1, li['answer1'])
            sheet2.write(i, 2, li['answer2'])
            sheet2.write(i, 3, li['answer3'])
            sheet2.write(i, 4, li['answer4'])
            sheet2.write(i, 5, li['classification'])
            sheet2.write(i, 6, li['dif'])
            i += 1

        for h in range(len(head3)):
            sheet3.write(0, h, head3[h])
        i = 1
        for li in demo.list3:
            sheet3.write(i, 0, li['question'])
            sheet3.write(i, 1, li['answer'])
            sheet3.write(i, 2, li['classification'])
            sheet3.write(i, 3, li['dif'])
            i += 1

        for h in range(len(head4)):
            sheet4.write(0, h, head4[h])
        i = 1
        for li in demo.list4:
            sheet4.write(i, 0, li['question'])
            sheet4.write(i, 1, li['choice1'])
            sheet4.write(i, 2, li['choice2'])
            sheet4.write(i, 3, li['choice3'])
            sheet4.write(i, 4, li['choice4'])
            sheet4.write(i, 5, li['answer'])
            sheet4.write(i, 6, li['analysis'])
            sheet4.write(i, 7, li['classification'])
            sheet4.write(i, 8, li['dif'])
            i += 1

        for h in range(len(head5)):
            sheet5.write(0, h, head5[h])
        i = 1
        for li in demo.list5:
            sheet5.write(i, 0, li['question'])
            sheet5.write(i, 1, li['choice1'])
            sheet5.write(i, 2, li['choice2'])
            sheet5.write(i, 3, li['choice3'])
            sheet5.write(i, 4, li['choice4'])
            sheet5.write(i, 5, li['answer'])
            sheet5.write(i, 6, li['analysis'])
            sheet5.write(i, 7, li['classification'])
            sheet5.write(i, 8, li['dif'])
            i += 1

        workbook.save('demo.xls')



if __name__ == '__main__':
    demo = Crawl()
    demo.get_datas()
    demo.save_sheet()
    # demo.dict1['question'] = demo.list1
    # demo.dict1['answer'] = demo.list2
    # demo.dict1['classification'] = demo.list3
    # demo.dict1['dif'] = demo.list4
    # print(demo.dict1)






