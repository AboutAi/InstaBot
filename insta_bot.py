from selenium import webdriver
from time import sleep
#instaBot Class
class InstaBot:
    #Constructor definition
    def __init__(self,user,pw,login,username=''):
        self.driver=webdriver.Chrome()
        self.username=user
        self.driver.get('https://instagram.com')
        if(login=='fb'):
            self.fb_login(username,pw)
        else:
            self.insta_direct_login(user,pw)
        while(len(self.driver.find_elements_by_xpath('//button[contains(text(),"Not Now")]'))<1):
            print('Not matched')
            sleep(2)
        self.driver.find_element_by_xpath('//button[contains(text(),"Not Now")]')\
            .click()
        sleep(3)
        self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input')\
            .send_keys('#cuteness')
        sleep(4)
        self.driver.find_element_by_xpath('/html/body/div[1]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]/div/div/div[1]/span')\
            .click()
        #Function for facebook login
    def fb_login(self,email,pw):
        sleep(5)
        self.driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[6]/button/span[2]').click()
        self.driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/form/div/div[1]/input')\
            .send_keys(email)
        self.driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/form/div/div[2]/input')\
            .send_keys(pw)
        self.driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/form/div/div[3]/button')\
            .click()
        #Function for direct login with facebook
    def insta_direct_login(self,user,pw):
        self.find('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input')\
            .send_keys(user)
        self.find('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input')\
            .send_keys(pw)
        self.find('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button')\
            .click()
        print('ok')
        #Function to open profile and getting follower and unfollower list
    def get_unfollower(self):
        sleep(10)
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}/')]".format(self.username))\
             .click()
        while(len(self.driver.find_elements_by_xpath("//a[contains(@href,'/{}/followers/')]".format(self.username)))<1):
            print('Not matched')
            sleep(2)
        while(len(self.driver.find_elements_by_xpath("//a[contains(@href,'/{}/following/')]".format(self.username)))<1):
            print('Not matched')
            sleep(2)
        sleep(4)
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}/followers/')]".format(self.username))\
             .click()
        sleep(2)
        followers=self.get_names()
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}/following/')]".format(self.username))\
             .click()
        following=self.get_names()
        not_following_back=[user for user in following if user not in followers]
        fwr_file=open('follower.txt','w')
        fwng_file=open('following.txt','w')
        nfd_back=open('Not-followed-back.txt','w')
        print('followers are: {} \n and following are: {} \n Not followed Back: {} \n'.format('\n'.join(followers),'\n'.join(following),'\n'.join(not_following_back)))
        fwr_file.write('followers are: {} \n and following are: {} \n Not followed Back: {} \n'.format('\n'.join(followers),'\n'.join(following),'\n'.join(not_following_back)))

        #Scrolling and Get text of link from div
    def get_names(self):
        sleep(4)
        scroll_box=self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]')
        last_ht,ht=0,1
        sleep(3)
        while last_ht!=ht:
            last_ht=ht
            sleep(3)
            ht=self.driver.execute_script("""
                                          arguments[0].scrollTo(0,arguments[0].scrollHeight);
                                          return arguments[0].scrollHeight;
                                          """,scroll_box)
            sleep(1)
        links=scroll_box.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul/div').find_elements_by_tag_name('a')
        names=[name.text for name in links if name.text!='']
        self.find('/html/body/div[4]/div/div[1]/div/div[2]/button')\
            .click()
        return names
    #Searching for an element till not found
    def find(self,xpath):
        while(len(self.driver.find_elements_by_xpath(xpath))<1):
            print('Not matched')
            sleep(2)
        sleep(4)
        return self.driver.find_element_by_xpath(xpath)
#Asking For Login Mode        
m=int(input('Mode of login : 1 for Facebook 2 for Instagram :'))
mybot=0
if(m==1):
    user,pw,username=map(str,input('Enter InstaUserName,password,FaceBookEmailId in a single line').split())
    mybot=InstaBot(user,pw,'fb',username)
else:
    user,pw=map(str,input('Enter InstaUserName, password in a single line').split())
    mybot=InstaBot(user,pw,'insta')
mybot.get_unfollower()
sleep(2)
