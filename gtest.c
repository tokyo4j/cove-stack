#include <sys/mman.h>
#include <signal.h>

#define NR_PAGES 64

int main() {
    char *ptr = mmap(0, 4096 * NR_PAGES, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    for(int i = 0; i < NR_PAGES; i++)
        ptr[4096 * i] = i;
    madvise(ptr, 4096 * NR_PAGES, 26);

    return 0;
}
