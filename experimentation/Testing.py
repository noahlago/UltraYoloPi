import torch

def torch_test():
    x = torch.rand(5, 3)
    print(x)    

def cuda_test():
    torch.cuda.is_available()

def main():
    torch_test()
    cuda_test()

if __name__ == "__main__":
    main()