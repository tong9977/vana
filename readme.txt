sudo mkdir /vanaramdisk
sudo mount -t tmpfs -o rw,size=2G tmpfs /vanaramdisk


sudo umount /vanaramdisk


sudo sysctl -w net.core.rmem_default=31457280
sudo sysctl -w net.core.rmem_max=33554432

sudo ip link set dev enp8s0 mtu 9000
sudo ip link set dev enp9s0 mtu 9000  


pip3 install opencv-python
pip3 install opencv-contrib-python