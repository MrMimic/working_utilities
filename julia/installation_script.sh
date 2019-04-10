
#!/usr/bin/env bash

# Download last version
cd ~
mkdir .julia
cd .julia
sudo apt-get install git
git clone git://github.com/JuliaLang/julia.git

# Parallel compilation
cd julia
make -j 4

# Add alias
echo "alias julia='~/.julia/julia/usr/bin/julia'" >> ~/.bashrc && source ~/.bashrc

# And now, let's instal Juno IDE
cd ~/.julia
mkdir atom && cd atom
wget "https://atom.io/download/deb"
sudo dpkg -i deb

# In Atom, go to Settings (Ctrl+,, or Cmd+, on macOS) and go to the "Install" panel.

# Type uber-juno into the search box and hit enter. Click the install button on the package of the same name.

# Atom will then set up Juno for you, installing the required Atom and Julia packages.
