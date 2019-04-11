/*
* CoolQ Demo for VC++ 
* Api Version 9
* Written by Coxxs & Thanks for the help of orzFly
*/

#include "stdafx.h"
#include "string"
#include "cqp.h"
#include "appmain.h" //应用AppID等信息，请正确填写，否则酷Q可能无法加载
#include "qq2word.h"
#include "UTF82GBK.h"
#include "qrencode.h"

#include <Windows.h>
#include <shellapi.h>
#include <tchar.h>
#include <fstream>
#include <sstream>
#include <map>
#pragma comment(lib,"qrencode.lib")

using namespace std;

int ac = -1; //AuthCode 调用酷Q的方法时需要用到
bool enabled = false;
string SAVE_PATH;
string url_base;
string suffix;

map<string, string> filmlist;

/* 
* 返回应用的ApiVer、Appid，打包后将不会调用
*/
CQEVENT(const char*, AppInfo, 0)() {
	return CQAPPINFO;
}


/* 
* 接收应用AuthCode，酷Q读取应用信息后，如果接受该应用，将会调用这个函数并传递AuthCode。
* 不要在本函数处理其他任何代码，以免发生异常情况。如需执行初始化代码请在Startup事件中执行（Type=1001）。
*/
CQEVENT(int32_t, Initialize, 4)(int32_t AuthCode) {
	ac = AuthCode;
	return 0;
}


/*
* Type=1001 酷Q启动
* 无论本应用是否被启用，本函数都会在酷Q启动后执行一次，请在这里执行应用初始化代码。
* 如非必要，不建议在这里加载窗口。（可以添加菜单，让用户手动打开窗口）
*/
CQEVENT(int32_t, __eventStartup, 0)() {
    ifstream csv(".\\film.csv");
    if (csv.is_open()) {
        csv.close();
        return 0;
    }

    wfstream file(".\\film.csv",ios::out);
    if (file.is_open()) {
        file << "电影名称" << "," << "网盘链接" << endl;
        file.close();
    }
    else {
        MessageBox(GetDesktopWindow(), _T("未能成功创建csv文件"), _T("警告"),MB_OK);
        file.close();
    }

    return 0;
}


/*
* Type=1002 酷Q退出
* 无论本应用是否被启用，本函数都会在酷Q退出前执行一次，请在这里执行插件关闭代码。
* 本函数调用完毕后，酷Q将很快关闭，请不要再通过线程等方式执行其他代码。
*/
CQEVENT(int32_t, __eventExit, 0)() {
	return 0;
}

/*
* Type=1003 应用已被启用
* 当应用被启用后，将收到此事件。
* 如果酷Q载入时应用已被启用，则在_eventStartup(Type=1001,酷Q启动)被调用后，本函数也将被调用一次。
* 如非必要，不建议在这里加载窗口。（可以添加菜单，让用户手动打开窗口）
*/
CQEVENT(int32_t, __eventEnable, 0)() {
	enabled = true;
    filmlist.clear();

    fstream csv(".\\film.csv", ios::in);
    if (!csv.is_open()) {
        MessageBox(NULL, _T("未能找到film.csv，请检查文件完整性"), _T("WARNING"), MB_OK);
        return 0;
    }

    string line;
    string film, link;
    getline(csv, line);
    while (getline(csv, line)) {
        stringstream ss(line);
        getline(ss, film, ',');
        getline(ss, link, ',');
        filmlist.insert(pair<string, string>(film, link));
    }
    csv.close();

    fstream setting(".\\setting",ios::in);
    if (!setting.is_open()) {
        MessageBox(GetDesktopWindow(), _T("严重错误:无法打开设置文件"), _T("警告"), MB_OK);
        setting.close();
        return 0;
    }
    /*getline(setting, SAVE_PATH);
    getline(setting, url_base);
    getline(setting, suffix);*/
    setting >> SAVE_PATH;
    setting >> url_base;
    setting >> suffix;
    setting.close();
	return 0;
}


/*
* Type=1004 应用将被停用
* 当应用被停用前，将收到此事件。
* 如果酷Q载入时应用已被停用，则本函数*不会*被调用。
* 无论本应用是否被启用，酷Q关闭前本函数都*不会*被调用。
*/
CQEVENT(int32_t, __eventDisable, 0)() {
	enabled = false;
	return 0;
}

/*
* Type=21 私聊消息
* subType 子类型，11/来自好友 1/来自在线状态 2/来自群 3/来自讨论组
*/
CQEVENT(int32_t, __eventPrivateMsg, 24)(int32_t subType, int32_t msgId, int64_t fromQQ, const char *msg, int32_t font) {

    string temp;
    string filename;
    char url[1024];
    

    size_t size;
    wchar_t *buffer=NULL;

    BOOL ret;
    SHELLEXECUTEINFO shellinfo;

    ifstream f;

    QRcode *code=nullptr;
    int pos;

	if (msg[0] == '#') {
        switch (msg[1]) {
        case '0':
            Sleep(500);
            CQ_sendPrivateMsg(ac, fromQQ,
                "帮助信息\n"
                "#0				---显示本帮助\n"
                "百度文库链接	---下载百度文库文档\n"
                "   列如：htt[CQ:face,id=14]ps://wenku[CQ:face,id=14].baidu.com/view/604e0b7b1711cc7931b7165f.html\n"
                "   电脑端直接复制需要下载的百度文库网址粘贴到qq发送\n"
                "   手机端按右上角的分享选择复制链接后粘贴到qq中发送\n\n"
                "#1+空格+电影名	---获得电影资源下载地址\n"
                "   列如：#1 白雪公主\n\n"
                "#2+空格+音乐名称	---下载高质量音乐\n"
                "   列如：#2 爱我中华\n"
                "本软件所转载的音视频等资料均为网络三方资源。"
            );
			return EVENT_BLOCK;

		case '1':
            Sleep(500);
            if (strlen(msg) <= 3) break;
            temp = string(msg);
            temp = temp.substr(3);
            //CQ_sendPrivateMsg(ac, fromQQ, temp.c_str());

            ret = true;
            for (map<string, string>::iterator iter = filmlist.begin(); iter != filmlist.end(); iter++) {
                if (iter->first.find(temp) != string::npos) {
                    CQ_sendPrivateMsg(ac, fromQQ, iter->second.c_str());
                    return EVENT_BLOCK;
                }   
                //CQ_sendPrivateMsg(ac, fromQQ, iter->first.c_str());
            }
            /*if (ret) {
                CQ_sendPrivateMsg(ac, fromQQ, "抱歉，未能找到相关电影");
            }*/
            temp = temp + " " + SAVE_PATH + "//" + qq2word(fromQQ)+" None";
            size = temp.length();
            buffer = new wchar_t[size + 1];
            MultiByteToWideChar(CP_ACP, 0, temp.c_str(), size, buffer, size * sizeof(wchar_t));
            buffer[size] = 0;
            //MessageBox(GetDesktopWindow(), buffer, _T("url"), MB_OK);

            ZeroMemory(&shellinfo, sizeof(shellinfo));
            shellinfo.cbSize = sizeof(SHELLEXECUTEINFO);
            shellinfo.fMask = SEE_MASK_NOCLOSEPROCESS;
            shellinfo.hwnd = GetDesktopWindow();
            shellinfo.lpVerb = _T("open");
            shellinfo.lpFile = _T("movie.exe");
            shellinfo.lpParameters = buffer;
            shellinfo.lpDirectory = _T(".\\downloader");
            shellinfo.nShow = SW_HIDE;
            shellinfo.hInstApp = NULL;

            ret = ShellExecuteEx(&shellinfo);
            WaitForSingleObject(shellinfo.hProcess, INFINITE);
            delete buffer;


            temp = url_base + qq2word(fromQQ) + "/BDPurl.html";
            QRTextConvate(temp, "../data/image/" + qq2word(fromQQ));
            temp = "[CQ:image,file=" + qq2word(fromQQ) + "\\QRcode.png]";
            CQ_sendPrivateMsg(ac, fromQQ, temp.c_str());

			break;
		case '2':
            if (strlen(msg) <= 3) break;
			CQ_sendPrivateMsg(ac, fromQQ, 
                "欢迎使用高品质MP3下载功能,注意:\n"
                "1.不能保证所有音乐均为最高品质\n"
                "2.不能保证100%下载成功,如果下载失败请重试,或者过段时间再试(或者放弃吐舌~)\n"
                "3.下载的资源仅供学习使用,请在下载完成后24h内删除\n"
                "正在下载,请稍等..."
            );

            temp = string(msg);
            memset(url, 0, sizeof(url));
            temp.copy(url, temp.length() - 3, 3);
            temp = "\""+string(url)+"\"";
            temp = temp + " " + SAVE_PATH + "/" + qq2word(fromQQ)+" \""+suffix+"\" None";

            size = temp.length();
            buffer = new wchar_t[size + 1];
            MultiByteToWideChar(CP_ACP, 0, temp.c_str(), size, buffer, size * sizeof(wchar_t));
            buffer[size] = 0;
            //MessageBox(GetDesktopWindow(), buffer, _T("url"), MB_OK);
            //delete buffer;

            ZeroMemory(&shellinfo, sizeof(shellinfo));
            shellinfo.cbSize = sizeof(SHELLEXECUTEINFO);
            shellinfo.fMask = SEE_MASK_NOCLOSEPROCESS;
            shellinfo.hwnd = GetDesktopWindow();
            shellinfo.lpVerb = _T("open");
            shellinfo.lpFile = _T("music.exe");
            shellinfo.lpParameters = buffer;
            shellinfo.lpDirectory = _T(".\\downloader");
            shellinfo.nShow = SW_HIDE;
            shellinfo.hInstApp = NULL;

            ret = ShellExecuteEx(&shellinfo);
            WaitForSingleObject(shellinfo.hProcess, INFINITE);
            delete buffer;

            if (!ret) {
                temp = to_string(GetLastError()) + "下载失败，请检查url重试或者联系机器人管理员";
                CQ_sendPrivateMsg(ac, fromQQ, temp.c_str());
                return EVENT_BLOCK;
            }

            CQ_sendPrivateMsg(ac, fromQQ, "下载完成，正在为您生成链接");
            
            
            
            temp = SAVE_PATH + "//" + qq2word(fromQQ) +" Welcome None";
            size = temp.length();
            buffer = new wchar_t[size + 1];
            MultiByteToWideChar(CP_ACP, 0, temp.c_str(), size, buffer, size * sizeof(wchar_t));
            buffer[size] = 0;

            ZeroMemory(&shellinfo, sizeof(shellinfo));
            shellinfo.cbSize = sizeof(SHELLEXECUTEINFO);
            shellinfo.fMask = SEE_MASK_NOCLOSEPROCESS;
            shellinfo.hwnd = GetDesktopWindow();
            shellinfo.lpVerb = _T("open");
            shellinfo.lpFile = _T("html.exe");
            shellinfo.lpParameters = buffer;
            shellinfo.lpDirectory = _T(".\\downloader");
            shellinfo.nShow = SW_HIDE;
            shellinfo.hInstApp = NULL;

            ret = ShellExecuteEx(&shellinfo);
            WaitForSingleObject(shellinfo.hProcess, INFINITE);
            delete buffer;

            if (!ret) {
                CQ_sendPrivateMsg(ac, fromQQ, "链接生成失败,请重试");
                return EVENT_BLOCK;
            }
            else {
                temp = url_base + qq2word(fromQQ);
                QRTextConvate(temp,  "../data/image/"+ qq2word(fromQQ));
                temp = "[CQ:image,file=" + qq2word(fromQQ) + "\\QRcode.png]";
                CQ_sendPrivateMsg(ac, fromQQ, temp.c_str());
            }
			break;
        /*case '3':
            CQ_sendPrivateMsg(ac, fromQQ, "■█");
            break;*/
		default:
			CQ_sendPrivateMsg(ac, fromQQ, "未能识别您的指令，请回复#0查看帮助信息(+_+)?");
			break;
		}
	}
	else {
        temp = string(msg);
        if (!(temp.find("https://wenku.baidu.com/view/") != string::npos || temp.find("https://wk.baidu.com/view/") !=string::npos || temp.find("https://m.baidu.com/sf_edu_wenku/view/")!=string::npos)) {
            CQ_sendPrivateMsg(ac, fromQQ, "更多功能，请回复#0查看帮助(英文井号)");
            return EVENT_BLOCK;
        }
        CQ_sendPrivateMsg(ac, fromQQ,
            "欢迎使用百度文库下载功能，注意：\n\n"
            "1.本功能无法下载百度文库中格式为pdf的文件\n"
            "2.本功能所下载的百度文库文档一律为pdf格式\n"
            "3.超过300页的文件可能会下载失败\n"
            "4.生成的下载链接有效期从下载时刻起至当日24：00"
            "\n请稍等片刻，正在下载文档..."
        );
        pos = temp.find("https://");
        temp = temp.substr(pos) + " " + SAVE_PATH + "//" + qq2word(fromQQ)+" 40 None";

        size = temp.length();
        buffer = new wchar_t[size + 1];
        MultiByteToWideChar(CP_ACP, 0, temp.c_str(), size, buffer, size * sizeof(wchar_t));
        buffer[size] = 0;
        //MessageBox(GetDesktopWindow(), buffer, _T("url"), MB_OK);
        //delete buffer;

        ZeroMemory(&shellinfo, sizeof(shellinfo));
        shellinfo.cbSize = sizeof(SHELLEXECUTEINFO);
        shellinfo.fMask = SEE_MASK_NOCLOSEPROCESS;
        shellinfo.hwnd = GetDesktopWindow();
        shellinfo.lpVerb = _T("open");
        shellinfo.lpFile = _T("BDWKdownload.exe");
        shellinfo.lpParameters = buffer;
        shellinfo.lpDirectory = _T(".\\downloader");
        shellinfo.nShow = SW_HIDE;
        shellinfo.hInstApp = NULL;

        ret = ShellExecuteEx(&shellinfo);
        WaitForSingleObject(shellinfo.hProcess, INFINITE);
        delete buffer;

        if (!ret) {
            temp = to_string(GetLastError()) + "下载失败，请检查url重试或者联系机器人管理员";
            CQ_sendPrivateMsg(ac, fromQQ, temp.c_str());
            return EVENT_BLOCK;
        }


        CQ_sendPrivateMsg(ac, fromQQ, "下载完成，正在为您生成链接");

        temp = SAVE_PATH + "//" + qq2word(fromQQ) + " Welcome None";
        size = temp.length();
        buffer = new wchar_t[size + 1];
        MultiByteToWideChar(CP_ACP, 0, temp.c_str(), size, buffer, size * sizeof(wchar_t));
        buffer[size] = 0;

        ZeroMemory(&shellinfo, sizeof(shellinfo));
        shellinfo.cbSize = sizeof(SHELLEXECUTEINFO);
        shellinfo.fMask = SEE_MASK_NOCLOSEPROCESS;
        shellinfo.hwnd = GetDesktopWindow();
        shellinfo.lpVerb = _T("open");
        shellinfo.lpFile = _T("html.exe");
        shellinfo.lpParameters = buffer;
        shellinfo.lpDirectory = _T(".\\downloader");
        shellinfo.nShow = SW_HIDE;
        shellinfo.hInstApp = NULL;

        ret = ShellExecuteEx(&shellinfo);
        WaitForSingleObject(shellinfo.hProcess, INFINITE);
        delete buffer;

        if (!ret) {
            CQ_sendPrivateMsg(ac, fromQQ, "链接生成失败,请重试");
            return EVENT_BLOCK;
        }
        else {
            temp = url_base + qq2word(fromQQ);
            QRTextConvate(temp, "../data/image/" + qq2word(fromQQ));
            temp = "[CQ:image,file=" + qq2word(fromQQ) + "\\QRcode.png]";
            CQ_sendPrivateMsg(ac, fromQQ, temp.c_str());
            Sleep(1000);
            CQ_sendPrivateMsg(ac, fromQQ, "如果您需要将pdf转换成其他格式可以访问如下网站");
            temp = "[CQ:image,file=PDFconvery.jpg]";
            CQ_sendPrivateMsg(ac, fromQQ, temp.c_str());

        }
        
	}
	
	//如果要回复消息，请调用酷Q方法发送，并且这里 return EVENT_BLOCK - 截断本条消息，不再继续处理  注意：应用优先级设置为"最高"(10000)时，不得使用本返回值
	//如果不回复消息，交由之后的应用/过滤器处理，这里 return EVENT_IGNORE - 忽略本条消息
	//return EVENT_IGNORE;
}


/*
* Type=2 群消息
*/
CQEVENT(int32_t, __eventGroupMsg, 36)(int32_t subType, int32_t msgId, int64_t fromGroup, int64_t fromQQ, const char *fromAnonymous, const char *msg, int32_t font) {

	string temp;
	string filename;
	char url[1024];


	size_t size;
	wchar_t *buffer = NULL;

	BOOL ret;
	SHELLEXECUTEINFO shellinfo;

	ifstream f;

	QRcode *code = nullptr;
	int pos;

	if (msg[0] == '#') {
		switch (msg[1]) {
		case '0':
			Sleep(500);
			CQ_sendGroupMsg(ac, fromGroup,
				"帮助信息\n"
				"#0				---显示本帮助\n"
				"百度文库链接	---下载百度文库文档\n"
				"   列如：htt[CQ:face,id=14]ps://wenku[CQ:face,id=14].baidu.com/view/604e0b7b1711cc7931b7165f.html\n"
				"   电脑端直接复制需要下载的百度文库网址粘贴到qq发送\n"
				"   手机端按右上角的分享选择复制链接后粘贴到qq中发送\n\n"
				"#1+空格+电影名	---获得电影资源下载地址\n"
				"   列如：#1 白雪公主\n\n"
				"#2+空格+音乐名称	---下载高质量音乐\n"
				"   列如：#2 爱我中华\n"
				"本软件所转载的音视频等资料均为网络三方资源。"
			);
			return EVENT_BLOCK;

		case '1':
			Sleep(500);
			if (strlen(msg) <= 3) break;
			temp = string(msg);
			temp = temp.substr(3);
			//CQ_sendGroupMsg(ac, fromGroup, temp.c_str());
			CQ_sendGroupMsg(ac, fromGroup, "链接二维码将通过私聊发送给您o(*￣▽￣*)o");

			ret = true;
			for (map<string, string>::iterator iter = filmlist.begin(); iter != filmlist.end(); iter++) {
				if (iter->first.find(temp) != string::npos) {
					CQ_sendPrivateMsg(ac, fromQQ, iter->second.c_str());
					return EVENT_BLOCK;
				}
				//CQ_sendGroupMsg(ac, fromGroup, iter->first.c_str());
			}
			/*if (ret) {
				CQ_sendGroupMsg(ac, fromGroup, "抱歉，未能找到相关电影");
			}*/
			temp = temp + " " + SAVE_PATH + "//" + qq2word(fromQQ) + " None";
			size = temp.length();
			buffer = new wchar_t[size + 1];
			MultiByteToWideChar(CP_ACP, 0, temp.c_str(), size, buffer, size * sizeof(wchar_t));
			buffer[size] = 0;
			//MessageBox(GetDesktopWindow(), buffer, _T("url"), MB_OK);

			ZeroMemory(&shellinfo, sizeof(shellinfo));
			shellinfo.cbSize = sizeof(SHELLEXECUTEINFO);
			shellinfo.fMask = SEE_MASK_NOCLOSEPROCESS;
			shellinfo.hwnd = GetDesktopWindow();
			shellinfo.lpVerb = _T("open");
			shellinfo.lpFile = _T("movie.exe");
			shellinfo.lpParameters = buffer;
			shellinfo.lpDirectory = _T(".\\downloader");
			shellinfo.nShow = SW_HIDE;
			shellinfo.hInstApp = NULL;

			ret = ShellExecuteEx(&shellinfo);
			WaitForSingleObject(shellinfo.hProcess, INFINITE);
			delete buffer;


			temp = url_base + qq2word(fromQQ) + "/BDPurl.html";
			QRTextConvate(temp, "../data/image/" + qq2word(fromQQ));
			temp = "[CQ:image,file=" + qq2word(fromQQ) + "\\QRcode.png]";
			CQ_sendPrivateMsg(ac, fromQQ, temp.c_str());

			break;
		case '2':
			if (strlen(msg) <= 3) break;
			CQ_sendGroupMsg(ac, fromGroup,
				"欢迎使用高品质MP3下载功能,注意:\n"
				"1.不能保证所有音乐均为最高品质\n"
				"2.不能保证100%下载成功,如果下载失败请重试,或者过段时间再试(或者放弃吐舌~)\n"
				"3.下载的资源仅供学习使用,请在下载完成后24h内删除\n"
				"正在下载,请稍等..."
			);

			temp = string(msg);
			memset(url, 0, sizeof(url));
			temp.copy(url, temp.length() - 3, 3);
			temp = "\"" + string(url) + "\"";
			temp = temp + " " + SAVE_PATH + "/" + qq2word(fromQQ) + " \"" + suffix + "\" None";

			size = temp.length();
			buffer = new wchar_t[size + 1];
			MultiByteToWideChar(CP_ACP, 0, temp.c_str(), size, buffer, size * sizeof(wchar_t));
			buffer[size] = 0;
			//MessageBox(GetDesktopWindow(), buffer, _T("url"), MB_OK);
			//delete buffer;

			ZeroMemory(&shellinfo, sizeof(shellinfo));
			shellinfo.cbSize = sizeof(SHELLEXECUTEINFO);
			shellinfo.fMask = SEE_MASK_NOCLOSEPROCESS;
			shellinfo.hwnd = GetDesktopWindow();
			shellinfo.lpVerb = _T("open");
			shellinfo.lpFile = _T("music.exe");
			shellinfo.lpParameters = buffer;
			shellinfo.lpDirectory = _T(".\\downloader");
			shellinfo.nShow = SW_HIDE;
			shellinfo.hInstApp = NULL;

			ret = ShellExecuteEx(&shellinfo);
			WaitForSingleObject(shellinfo.hProcess, INFINITE);
			delete buffer;

			if (!ret) {
				temp = to_string(GetLastError()) + "下载失败，请检查url重试或者联系机器人管理员";
				CQ_sendGroupMsg(ac, fromGroup, temp.c_str());
				return EVENT_BLOCK;
			}

			CQ_sendGroupMsg(ac, fromGroup, "下载完成，正在为您生成链接,链接二维码将通过私聊二维码发送");



			temp = SAVE_PATH + "//" + qq2word(fromQQ) + " Welcome None";
			size = temp.length();
			buffer = new wchar_t[size + 1];
			MultiByteToWideChar(CP_ACP, 0, temp.c_str(), size, buffer, size * sizeof(wchar_t));
			buffer[size] = 0;

			ZeroMemory(&shellinfo, sizeof(shellinfo));
			shellinfo.cbSize = sizeof(SHELLEXECUTEINFO);
			shellinfo.fMask = SEE_MASK_NOCLOSEPROCESS;
			shellinfo.hwnd = GetDesktopWindow();
			shellinfo.lpVerb = _T("open");
			shellinfo.lpFile = _T("html.exe");
			shellinfo.lpParameters = buffer;
			shellinfo.lpDirectory = _T(".\\downloader");
			shellinfo.nShow = SW_HIDE;
			shellinfo.hInstApp = NULL;

			ret = ShellExecuteEx(&shellinfo);
			WaitForSingleObject(shellinfo.hProcess, INFINITE);
			delete buffer;

			if (!ret) {
				CQ_sendGroupMsg(ac, fromGroup, "链接生成失败,请重试");
				return EVENT_BLOCK;
			}
			else {
				temp = url_base + qq2word(fromQQ);
				QRTextConvate(temp, "../data/image/" + qq2word(fromQQ));
				temp = "[CQ:image,file=" + qq2word(fromQQ) + "\\QRcode.png]";
				CQ_sendPrivateMsg(ac, fromQQ, temp.c_str());
			}
			break;
			/*case '3':
				CQ_sendPrivateMsg(ac, fromQQ, "■█");
				break;*/
		default:
			CQ_sendGroupMsg(ac, fromGroup, "未能识别您的指令，请回复#0查看帮助信息(+_+)?");
			break;
		}
	}
	else {
		temp = string(msg);
		if (!(temp.find("https://wenku.baidu.com/view/") != string::npos || temp.find("https://wk.baidu.com/view/") != string::npos || temp.find("https://m.baidu.com/sf_edu_wenku/view/") != string::npos)) {
			/*CQ_sendGroupMsg(ac, fromGroup, "更多功能，请回复#0查看帮助(英文井号)");*/
			return EVENT_BLOCK;
		}
		CQ_sendGroupMsg(ac, fromGroup,
			"欢迎使用百度文库下载功能，注意：\n\n"
			"1.本功能无法下载百度文库中格式为pdf的文件\n"
			"2.本功能所下载的百度文库文档一律为pdf格式\n"
			"3.超过300页的文件可能会下载失败\n"
			"4.生成的下载链接有效期从下载时刻起至当日24：00"
			"\n请稍等片刻，正在下载文档..."
		);
		pos = temp.find("https://");
		temp = temp.substr(pos) + " " + SAVE_PATH + "//" + qq2word(fromQQ) + " 40 None";

		size = temp.length();
		buffer = new wchar_t[size + 1];
		MultiByteToWideChar(CP_ACP, 0, temp.c_str(), size, buffer, size * sizeof(wchar_t));
		buffer[size] = 0;
		//MessageBox(GetDesktopWindow(), buffer, _T("url"), MB_OK);
		//delete buffer;

		ZeroMemory(&shellinfo, sizeof(shellinfo));
		shellinfo.cbSize = sizeof(SHELLEXECUTEINFO);
		shellinfo.fMask = SEE_MASK_NOCLOSEPROCESS;
		shellinfo.hwnd = GetDesktopWindow();
		shellinfo.lpVerb = _T("open");
		shellinfo.lpFile = _T("BDWKdownload.exe");
		shellinfo.lpParameters = buffer;
		shellinfo.lpDirectory = _T(".\\downloader");
		shellinfo.nShow = SW_HIDE;
		shellinfo.hInstApp = NULL;

		ret = ShellExecuteEx(&shellinfo);
		WaitForSingleObject(shellinfo.hProcess, INFINITE);
		delete buffer;

		if (!ret) {
			temp = to_string(GetLastError()) + "下载失败，请检查url重试或者联系机器人管理员";
			CQ_sendGroupMsg(ac, fromGroup, temp.c_str());
			return EVENT_BLOCK;
		}


		CQ_sendGroupMsg(ac, fromGroup, "下载完成，正在为您生成链接,链接二维码将通过私聊二维码发送");

		temp = SAVE_PATH + "//" + qq2word(fromQQ) + " Welcome None";
		size = temp.length();
		buffer = new wchar_t[size + 1];
		MultiByteToWideChar(CP_ACP, 0, temp.c_str(), size, buffer, size * sizeof(wchar_t));
		buffer[size] = 0;

		ZeroMemory(&shellinfo, sizeof(shellinfo));
		shellinfo.cbSize = sizeof(SHELLEXECUTEINFO);
		shellinfo.fMask = SEE_MASK_NOCLOSEPROCESS;
		shellinfo.hwnd = GetDesktopWindow();
		shellinfo.lpVerb = _T("open");
		shellinfo.lpFile = _T("html.exe");
		shellinfo.lpParameters = buffer;
		shellinfo.lpDirectory = _T(".\\downloader");
		shellinfo.nShow = SW_HIDE;
		shellinfo.hInstApp = NULL;

		ret = ShellExecuteEx(&shellinfo);
		WaitForSingleObject(shellinfo.hProcess, INFINITE);
		delete buffer;

		if (!ret) {
			CQ_sendGroupMsg(ac, fromGroup, "链接生成失败,请重试");
			return EVENT_BLOCK;
		}
		else {
			temp = url_base + qq2word(fromQQ);
			QRTextConvate(temp, "../data/image/" + qq2word(fromQQ));
			temp = "[CQ:image,file=" + qq2word(fromQQ) + "\\QRcode.png]";
			CQ_sendPrivateMsg(ac, fromQQ, temp.c_str());
			Sleep(1000);
			CQ_sendPrivateMsg(ac, fromQQ, "如果您需要将pdf转换成其他格式可以访问如下网站");
			temp = "[CQ:image,file=PDFconvery.jpg]";
			CQ_sendPrivateMsg(ac, fromQQ, temp.c_str());

		}

	}
}


/*
* Type=4 讨论组消息
*/
CQEVENT(int32_t, __eventDiscussMsg, 32)(int32_t subType, int32_t msgId, int64_t fromDiscuss, int64_t fromQQ, const char *msg, int32_t font) {

	return EVENT_IGNORE; //关于返回值说明, 见“_eventPrivateMsg”函数
}


/*
* Type=101 群事件-管理员变动
* subType 子类型，1/被取消管理员 2/被设置管理员
*/
CQEVENT(int32_t, __eventSystem_GroupAdmin, 24)(int32_t subType, int32_t sendTime, int64_t fromGroup, int64_t beingOperateQQ) {

	return EVENT_IGNORE; //关于返回值说明, 见“_eventPrivateMsg”函数
}


/*
* Type=102 群事件-群成员减少
* subType 子类型，1/群员离开 2/群员被踢 3/自己(即登录号)被踢
* fromQQ 操作者QQ(仅subType为2、3时存在)
* beingOperateQQ 被操作QQ
*/
CQEVENT(int32_t, __eventSystem_GroupMemberDecrease, 32)(int32_t subType, int32_t sendTime, int64_t fromGroup, int64_t fromQQ, int64_t beingOperateQQ) {

	return EVENT_IGNORE; //关于返回值说明, 见“_eventPrivateMsg”函数
}


/*
* Type=103 群事件-群成员增加
* subType 子类型，1/管理员已同意 2/管理员邀请
* fromQQ 操作者QQ(即管理员QQ)
* beingOperateQQ 被操作QQ(即加群的QQ)
*/
CQEVENT(int32_t, __eventSystem_GroupMemberIncrease, 32)(int32_t subType, int32_t sendTime, int64_t fromGroup, int64_t fromQQ, int64_t beingOperateQQ) {

	return EVENT_IGNORE; //关于返回值说明, 见“_eventPrivateMsg”函数
}


/*
* Type=201 好友事件-好友已添加
*/
CQEVENT(int32_t, __eventFriend_Add, 16)(int32_t subType, int32_t sendTime, int64_t fromQQ) {

	return EVENT_IGNORE; //关于返回值说明, 见“_eventPrivateMsg”函数
}


/*
* Type=301 请求-好友添加
* msg 附言
* responseFlag 反馈标识(处理请求用)
*/
CQEVENT(int32_t, __eventRequest_AddFriend, 24)(int32_t subType, int32_t sendTime, int64_t fromQQ, const char *msg, const char *responseFlag) {

	//CQ_setFriendAddRequest(ac, responseFlag, REQUEST_ALLOW, "");

	return EVENT_IGNORE; //关于返回值说明, 见“_eventPrivateMsg”函数
}


/*
* Type=302 请求-群添加
* subType 子类型，1/他人申请入群 2/自己(即登录号)受邀入群
* msg 附言
* responseFlag 反馈标识(处理请求用)
*/
CQEVENT(int32_t, __eventRequest_AddGroup, 32)(int32_t subType, int32_t sendTime, int64_t fromGroup, int64_t fromQQ, const char *msg, const char *responseFlag) {

	//if (subType == 1) {
	//	CQ_setGroupAddRequestV2(ac, responseFlag, REQUEST_GROUPADD, REQUEST_ALLOW, "");
	//} else if (subType == 2) {
	//	CQ_setGroupAddRequestV2(ac, responseFlag, REQUEST_GROUPINVITE, REQUEST_ALLOW, "");
	//}

	return EVENT_IGNORE; //关于返回值说明, 见“_eventPrivateMsg”函数
}

/*
* 菜单，可在 .json 文件中设置菜单数目、函数名
* 如果不使用菜单，请在 .json 及此处删除无用菜单
*/
CQEVENT(int32_t, savePath_setting, 0)() {
	//MessageBoxA(NULL, "这是menuA，在这里载入窗口，或者进行其他工作。", "" ,0);
    wchar_t *buffer;
    string temp = SAVE_PATH;
    size_t size = temp.length();
    buffer = new wchar_t[size + 1];
    MultiByteToWideChar(CP_ACP, 0, temp.c_str(), size, buffer, size * sizeof(wchar_t));
    buffer[size] = 0;
    MessageBox(GetDesktopWindow(), buffer, _T("文件保存目录"), MB_OK);
    delete buffer;
    return 0;
}

CQEVENT(int32_t, URL_setting, 0)() {
    wchar_t *buffer;
    string temp = url_base;
    size_t size = temp.length();
    buffer = new wchar_t[size + 1];
    MultiByteToWideChar(CP_ACP, 0, temp.c_str(), size, buffer, size * sizeof(wchar_t));
    buffer[size] = 0;
    MessageBox(GetDesktopWindow(), buffer, _T("WEB URL"), MB_OK);
    delete buffer;
	return 0;
}

CQEVENT(int32_t, suffix_setting, 0)() {
    wchar_t *buffer;
    string temp = suffix;
    size_t size = temp.length();
    buffer = new wchar_t[size + 1];
    MultiByteToWideChar(CP_ACP, 0, temp.c_str(), size, buffer, size * sizeof(wchar_t));
    buffer[size] = 0;
    MessageBox(GetDesktopWindow(), buffer, _T("WEB URL"), MB_OK);
    delete buffer;
    return 0;
}


CQEVENT(int32_t, about_setting, 0)() {
    MessageBoxA(
        GetDesktopWindow(),
        "修改如上设置请到酷q目录下的setting.txt中\n"
        "code by cc 2019.1.20",
        "关于", 0);
    return 0;
}

