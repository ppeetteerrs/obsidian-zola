FROM alpine
RUN apk --update add git zola python3 rsync py3-pip curl g++ && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    pip3 install python-slugify rtoml && \
    git clone https://github.com/ppeetteerrs/obsidian-zola && \
    mkdir /obsidian
ENV VAULT=/obsidian
RUN curl -sSf https://sh.rustup.rs | sh -s -- -y && \
    source ~/.cargo/env && \ 
    cargo install obsidian-export
ENV PATH="$HOME/.cargo/bin:$PATH"
COPY entrypoint.sh /
RUN cp $HOME/.cargo/bin/obsidian-export /obsidian-zola/bin/obsidian-export && \
    sed -i 's|zola --root=build serve|zola --root=build serve --interface 0.0.0.0 --base-url $SITE_URL|' /obsidian-zola/local-run.sh && \
    chmod +x /entrypoint.sh

EXPOSE 1111
WORKDIR /obsidian-zola
#ENTRYPOINT ["tail", "-f", "/dev/null"]
ENTRYPOINT [ "/entrypoint.sh" ]
#CMD []
