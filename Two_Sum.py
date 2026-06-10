class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        
        num_to_index = {}
        
        for current_index, num in enumerate(nums):
           
            complement = target - num
            
            if complement in num_to_index:
        
                return [num_to_index[complement], current_index]
            
         
            num_to_index[num] = current_index
            
        return []  # Return empty list if no solution is found