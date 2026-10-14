#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include <iomanip>

#ifdef _WIN32
#define OPEN_CMD "start \"\" "
#else
#ifdef __APPLE__
#define OPEN_CMD "open "
#else
#define OPEN_CMD "xdg-open "
#endif
#endif

struct Link { std::string name; std::string url; };

static std::string urlenc(const std::string& s) {
    std::ostringstream o;
    for (unsigned char c : s) {
        if (isalnum(c) || c=='-'||c=='_'||c=='.'||c=='~') o << c;
        else o << '%' << std::hex << std::uppercase << (int)c;
    }
    return o.str();
}

static void open_url(const std::string& u) {
    std::string cmd = std::string(OPEN_CMD) + "\"" + u + "\"";
    std::cout << " -> " << u << "\n";
    std::system(cmd.c_str());
}

static std::string file_md5_note(const std::string& path) {
    std::ifstream f(path, std::ios::binary);
    if (!f) return "file not found";
    // simple FNV hash (note: not real md5, keeps no-dep build)
    unsigned long long h = 1469598103934665603ULL;
    char b[4096]; std::streamsize n; size_t total = 0;
    while ((n = f.readsome(b, sizeof b)) > 0) { total += (size_t)n; for (int i=0;i<n;i++){ h ^= (unsigned char)b[i]; h *= 1099511628211ULL; } }
    std::ostringstream o; o << "size=" << total << " fnv=0x" << std::hex << h << " (use md5sum for exact hash)";
    return o.str();
}

int main() {
    std::cout << "==============================\n AllSee OSINT (C++ edition)\n==============================\n";
    std::cout << "Type what you know: a name, a @username,\na phone number, an email, or a photo file.\n\n";
    while (true) {
        std::cout << "\n[1] Search a name / username / phone / email\n[2] Search by photo (opens reverse-image sites)\n[3] Quit\nChoice: ";
        std::string c; if (!std::getline(std::cin, c)) break;
        if (c == "3" || c == "q") break;
        if (c == "2") {
            std::cout << "Photo file path (or ENTER to just open upload pages): ";
            std::string p; if (!std::getline(std::cin, p)) break;
            if (!p.empty()) std::cout << "File: " << file_md5_note(p) << "\n";
            std::cout << "\nOpening upload pages. Pick one, drop the photo in.\n";
            std::vector<Link> L = {
                {"Google Lens", "https://lens.google.com/"},
                {"Bing Visual", "https://www.bing.com/visualsearch"},
                {"Yandex Images", "https://yandex.com/images-apphost/image-download"},
                {"TinEye", "https://tineye.com/"},
                {"Pimeyes (faces)", "https://pimeyes.com/en"},
                {"FaceCheck (faces)", "https://facecheck.id/"},
            };
            for (size_t i = 0; i < L.size(); i++) std::cout << " " << (i+1) << ". " << L[i].name << "\n";
            std::cout << "Open all? (y/n): ";
            std::string a; if (!std::getline(std::cin, a)) break;
            if (a == "y" || a == "Y") for (auto& l : L) open_url(l.url);
            else { std::cout << "Number to open: "; std::string n; if (!std::getline(std::cin, n)) break; int k = atoi(n.c_str()); if (k>=1 && k<=(int)L.size()) open_url(L[k-1].url); }
            continue;
        }
        std::cout << "Enter it: ";
        std::string q; if (!std::getline(std::cin, q)) break;
        if (q.empty()) continue;
        std::string e = urlenc(q);
        std::vector<Link> L = {
            {"Google", "https://www.google.com/search?q=\"" + e + "\""},
            {"Bing", "https://www.bing.com/search?q=\"" + e + "\""},
            {"Google Images", "https://www.google.com/search?tbm=isch&q=\"" + e + "\""},
            {"Yandex (good for faces)", "https://yandex.com/images/search?text=" + e},
            {"People finder (WebMii)", "https://webmii.com/people?n=\"" + e + "\""},
            {"GitHub code (leaks)", "https://github.com/search?q=%22" + e + "%22&type=code"},
            {"Maps / business", "https://www.google.com/maps/search/" + e},
        };
        std::cout << "\nI will open public search pages for: " << q << "\n";
        for (size_t i = 0; i < L.size(); i++) std::cout << " " << (i+1) << ". " << L[i].name << "\n";
        std::cout << " 8. Open ALL\nNumber: ";
        std::string n; if (!std::getline(std::cin, n)) break;
        int k = atoi(n.c_str());
        if (k == 8) for (auto& l : L) open_url(l.url);
        else if (k >= 1 && k <= (int)L.size()) open_url(L[k-1].url);
        else std::cout << "ok, skipped.\n";
    }
    std::cout << "bye!\n";
    return 0;
}
