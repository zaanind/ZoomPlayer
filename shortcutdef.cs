using System;
using System.Runtime.InteropServices;

public class HotKey
{
    [DllImport("user32.dll")]
    public static extern bool RegisterHotKey(IntPtr hWnd, int id, int fsModifiers, int vlc);

    public static void RegisterHotKey(int key, int modifier, IntPtr hWnd)
    {
        RegisterHotKey(hWnd, 0, modifier, key);
    }
}
