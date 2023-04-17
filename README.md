---
title: Milestone 3
emoji: 🔥
colorFrom: indigo
colorTo: blue
sdk: streamlit
sdk_version: 1.17.0
app_file: app.py
pinned: false
license: openrail
---

# This is the Hugging Face link: https://huggingface.co/spaces/EthanDiaz03/Milestone_3/tree/main

# Interpretable-Gradient-Boosting---Real-Estate-House-Price-Prediction
Docker Desktop WSL 2 backend on Windows
Windows Subsystem for Linux (WSL) 2 is a full Linux kernel built by Microsoft, which allows Linux distributions to run without managing virtual machines. With Docker Desktop running on WSL 2, users can leverage Linux workspaces and avoid maintaining both Linux and Windows build scripts. In addition, WSL 2 provides improvements to file system sharing and boot time.

Docker Desktop uses the dynamic memory allocation feature in WSL 2 to improve the resource consumption. This means, Docker Desktop only uses the required amount of CPU and memory resources it needs, while enabling CPU and memory-intensive tasks such as building a container, to run much faster.

Additionally, with WSL 2, the time required to start a Docker daemon after a cold start is significantly faster. It takes less than 10 seconds to start the Docker daemon compared to almost a minute in the previous version of Docker Desktop.

Prerequisites
Before you turn on the Docker Desktop WSL 2, ensure you have:

Windows 10, version 1903 or higher, or Windows 11.
Enabled WSL 2 feature on Windows. For detailed instructions, refer to the Microsoft documentation.
Downloaded and installed the Linux kernel update package.
Turn on Docker Desktop WSL 2
Download Docker Desktop for Windows.
Follow the usual installation instructions to install Docker Desktop. If you are running a supported system, Docker Desktop prompts you to enable WSL 2 during installation. Read the information displayed on the screen and enable WSL 2 to continue.
Start Docker Desktop from the Windows Start menu.
From the Docker menu, select Settings and then General.
Select the Use WSL 2 based engine check box.

If you have installed Docker Desktop on a system that supports WSL 2, this option is enabled by default.

Select Apply & Restart.
Now docker commands work from Windows using the new WSL 2 engine.

Enabling Docker support in WSL 2 distros
WSL 2 adds support for “Linux distros” to Windows, where each distro behaves like a VM except they all run on top of a single shared Linux kernel.

Docker Desktop does not require any particular Linux distros to be installed. The docker CLI and UI all work fine from Windows without any additional Linux distros. However for the best developer experience, we recommend installing at least one additional distro and enabling Docker support by:

Ensure the distribution runs in WSL 2 mode. WSL can run distributions in both v1 or v2 mode.

To check the WSL mode, run:


 wsl.exe -l -v
To upgrade your existing Linux distro to v2, run:


 wsl.exe --set-version (distro name) 2
To set v2 as the default version for future installations, run:


 wsl.exe --set-default-version 2
When Docker Desktop starts, go to Settings > Resources > WSL Integration.

The Docker-WSL integration is enabled on your default WSL distribution. To change your default WSL distro, run wsl --set-default <distro name>

For example, to set Ubuntu as your default WSL distro, run:


 wsl --set-default ubuntu
Optionally, select any additional distributions you would like to enable the Docker-WSL integration on.

Select Apply & Restart.

Note

Docker Desktop installs two special-purpose internal Linux distros docker-desktop and docker-desktop-data. The first (docker-desktop) is used to run the Docker engine (dockerd) while the second (docker-desktop-data) stores containers and images. Neither can be used for general development.

Best practices
To get the best out of the file system performance when bind-mounting files, we recommend storing source code and other data that is bind-mounted into Linux containers, for instance with docker run -v <host-path>:<container-path>, in the Linux file system, rather than the Windows file system. You can also refer to the recommendation from Microsoft.

Linux containers only receive file change events, “inotify events”, if the original files are stored in the Linux filesystem. For example, some web development workflows rely on inotify events for automatic reloading when files have changed.
Performance is much higher when files are bind-mounted from the Linux filesystem, rather than remoted from the Windows host. Therefore avoid docker run -v /mnt/c/users:/users, where /mnt/c is mounted from Windows.
Instead, from a Linux shell use a command like docker run -v ~/my-project:/sources <my-image> where ~ is expanded by the Linux shell to $HOME.
If you have concerns about the size of the docker-desktop-data VHDX, or need to change it, take a look at the WSL tooling built into Windows.
If you have concerns about CPU or memory usage, you can configure limits on the memory, CPU, and swap size allocated to the WSL 2 utility VM.
To avoid any potential conflicts with using WSL 2 on Docker Desktop, you must uninstall any previous versions of Docker Engine and CLI installed directly through Linux distributions before installing Docker Desktop.
Develop with Docker and WSL 2
The following section describes how to start developing your applications using Docker and WSL 2. We recommend that you have your code in your default Linux distribution for the best development experience using Docker and WSL 2. After you have enabled WSL 2 on Docker Desktop, you can start working with your code inside the Linux distro and ideally with your IDE still in Windows. This workflow is straightforward if you are using VSCode.

Open VS Code and install the Remote - WSL extension. This extension allows you to work with a remote server in the Linux distro and your IDE client still on Windows.
Now, you can start working in VS Code remotely. To do this, open your terminal and type:


 wsl

 code .
This opens a new VS Code connected remotely to your default Linux distro which you can check in the bottom corner of the screen.

Alternatively, you can type the name of your default Linux distro in your Start menu, open it, and then run code .

When you are in VS Code, you can use the terminal in VS Code to pull your code and start working natively from your Windows machine.
![image](https://user-images.githubusercontent.com/125219648/227837042-9fd504f7-7a42-4778-860a-8e9503a138b0.png)
