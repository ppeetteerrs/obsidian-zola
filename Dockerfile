FROM alpine

RUN apk --update add git zola python3 rsync py3-pip curl g++
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN pip3 install python-slugify rtoml
RUN git clone https://github.com/ppeetteerrs/obsidian-zola
WORKDIR /obsidian
WORKDIR /obsidian-zola
ENV VAULT=/obsidian
RUN curl -sSf https://sh.rustup.rs | sh -s -- -y && \
    source ~/.cargo/env && \ 
    cargo install obsidian-export
ENV PATH="$HOME/.cargo/bin:$PATH"
RUN cp /obsidian-zola/netlify.example.toml /obsidian/netlify.toml && \
    cp $HOME/.cargo/bin/obsidian-export /obsidian-zola/bin/obsidian-export && \
    sed -i 's|SITE_URL = ""|SITE_URL = "'$SITE_URL'"|' /obsidian/netlify.toml && \
    sed -i 's|zola --root=build serve|zola --root=build serve --interface 0.0.0.0 --base-url $SITE_URL|' /obsidian-zola/local-run.sh 

EXPOSE 1111
ENTRYPOINT ["tail", "-f", "/dev/null"]
