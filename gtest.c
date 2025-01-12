#include <sys/mman.h>
#include <unistd.h>
#include <stdio.h>
#include <stdint.h>

#define NR_PAGES (256 * 32) // 32MB

int main() {
    char *ptr = mmap(0, 4096 * NR_PAGES, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    for(uint32_t i = 0; i < NR_PAGES; i++)
        *(uint32_t *)&ptr[4096 * i] = i;
    madvise(ptr, 4096 * NR_PAGES, 26);

    puts("Entering infinite loop...");

    while(1){}

    return 0;
}
