#pragma once
#include<Windows.h>
#include<string>
#include<shellapi.h>
#include<tchar.h>
using namespace std;
#define W 651

string UTF8ToGBK(const char* str)
{
    string result;
    WCHAR *strSrc;
    LPSTR szRes;

    //获得临时变量的大小
    int i = MultiByteToWideChar(CP_UTF8, 0, str, -1, NULL, 0);
    strSrc = new WCHAR[i + 1];
    MultiByteToWideChar(CP_UTF8, 0, str, -1, strSrc, i);

    //获得临时变量的大小
    i = WideCharToMultiByte(CP_ACP, 0, strSrc, -1, NULL, 0, NULL, NULL);
    szRes = new CHAR[i + 1];
    WideCharToMultiByte(CP_ACP, 0, strSrc, -1, szRes, i, NULL, NULL);

    result = szRes;
    delete[]strSrc;
    delete[]szRes;

    return result;
}


void QRTextConvate(string words,string filename) {
    SHELLEXECUTEINFO shellinfo;

    string temp = words + " " + filename+" None";
    size_t size = temp.length();
    wchar_t* buffer = new wchar_t[size + 1];
    MultiByteToWideChar(CP_ACP, 0, temp.c_str(), size, buffer, size * sizeof(wchar_t));
    buffer[size] = 0;
    //MessageBox(GetDesktopWindow(), buffer, _T("url"), MB_OK);

    ZeroMemory(&shellinfo, sizeof(shellinfo));
    shellinfo.cbSize = sizeof(SHELLEXECUTEINFO);
    shellinfo.fMask = SEE_MASK_NOCLOSEPROCESS;
    shellinfo.hwnd = GetDesktopWindow();
    shellinfo.lpVerb = _T("open");
    shellinfo.lpFile = _T("QR.exe");
    shellinfo.lpParameters = buffer;
    shellinfo.lpDirectory = _T(".\\downloader");
    shellinfo.nShow = SW_HIDE;
    shellinfo.hInstApp = NULL;

    BOOL ret = ShellExecuteEx(&shellinfo);
    WaitForSingleObject(shellinfo.hProcess, INFINITE);
    delete buffer;
    return;
}
