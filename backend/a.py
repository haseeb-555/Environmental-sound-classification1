class Solution:
    def findMaxConsecutiveOnes(self, nums):
        a=0
        b=[]
        for i in nums:
            if i==1:
                a=a+1
            elif i==0:
                b.append(a)
                a=0
        print(max(b))
        return(max(b))
nums=[1,1,0,1,1,1]
Solution=Solution()
Solution.findMaxConsecutiveOnes(nums)