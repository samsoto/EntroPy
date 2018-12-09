# Entropy Wiki

| **Type**            | **Equation**                                                                                     | **Venn Diagram**                                                                                  |
|---------------------|--------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------:|
| [Entropy](https://github.com/samsoto/EntroPy/blob/master/readme.md#entropy)             | ![](./resources/images/tex_entropy.png)             |                                                                                                   |
| [Cross Entropy](https://github.com/samsoto/EntroPy/blob/master/readme.md#cross-entropy)     |
| [Relative Entropy](https://github.com/samsoto/EntroPy/blob/master/readme.md#entropy-equation)       | ![](./resources/images/tex_cross_entropy.png)    | ![](./resources/images/tex_relative_entropy.png)    | ![](./resources/images/venn_relative_entropy.png)    |
| [Joint Entropy]       | ![](./resources/images/tex_joint_entropy.png)       | ![](./resources/images/venn_joint_entropy.png)       |
| [Conditional Entropy] | ![](./resources/images/tex_conditional_entropy.png) | ![](./resources/images/venn_conditional_entropy.png) |
| [Mutual Information]  | ![](./resources/images/tex_mutual_information.png)  | ![](./resources/images/venn_mutual_information.png)  |


# Entropy

Information entropy is the average rate at which information is produced by a stochastic source of data. The measure of information entropy associated with each possible data value

![](./resources/images/tex_entropy.png)

## What is Entropy?

Entropy is a measure of how unpredictable something is. **High Unpredictability, High Entropy.** An example of high entropy is an orinary coin, say a quarter. If you're asked to predict the next coin flip what would you choose? It's 50-50 chance of heads or tails so the best you can do is randomly guess. The situation is unpredictable so it has **High Entropy**. Now lets consider a different example and image you opened a book and, without looking, point to a random letter anywhere in the book. If you were told you would win a million dollars if you can  correctly guess the letter. What letter would you choose? Looking at the leter frequencies for English we can see that some letter are more frequent than others. Thus we have some predictability and the entopry is not as high as a situation where each letter was equally likely.

![](./resources/images/entropy_intro/letter_frequency.png)




### **Relationship between Probabilities and YES/NO Questions**

We will now explain how **Unpredictability** and **Entropy.** are related. 

![](./resources/images/entropy_intro/tree_basic.png)


### Set 1

![](./resources/images/entropy_intro/symbol_a_alice_bob.png)


| ![](./resources/images/entropy_intro/symbol_a_questons.png) | ![](resources/images/entropy_intro/symbol_a_num_questions_2.png) |
|-------------------------------------------------------------|-------------------------------------------------------------|

### Set 2

![](./resources/images/entropy_intro/symbol_b_alice_bob.png)

| ![](./resources/images/entropy_intro/symbol_b_questons.png) | ![](./resources/images/entropy_intro/symbol_b_num_questions.png) |
|-------------------------------------------------------------|-------------------------------------------------------------|

# Entropy Equation

![](./resources/images/entropy_intro/entropy_explain_1.png)

![](./resources/images/entropy_intro/entropy_explain_2.png)

![](./resources/images/entropy_intro/entropy_explain_3.png)



 
# Cross Entropy

In information theory, the cross entropy between two probability distributions *p* and *q* over the same underlying set of events measures the average number of bits needed to identify an event drawn from the set, if a coding scheme is used that is optimized for an "artificial" probability distribution *q*, rather than the "true" distribution *p*.

![](./resources/images/venn_cross_entropy_2.png)

![](./resources/images/tex_cross_entropy.png)

# Relative Entropy 
### ***(Kullback-Liebler Divergence)***


In mathematical statistics, the Kullback–Leibler divergence (also called relative entropy) is a measure of how one probability distribution is different from a second, reference probability distribution.

![](./resources/images/venn_relative_entropy.png)

![](./resources/images/tex_relative_entropy.png)

# Join Entropy

In information theory, joint entropy is a measure of the uncertainty associated with a set of variables.

![](./resources/images/venn_joint_entropy.png)

![](./resources/images/tex_joint_entropy.png)


# Conditional Entropy

n information theory, the conditional entropy (or equivocation) quantifies the amount of information needed to describe the outcome of a random variable *y* given that the value of another random variable *x* is known.

![](./resources/images/venn_conditional_entropy.png)

![](./resources/images/tex_conditional_entropy.png)

# Mutual Information

In probability theory and information theory, the mutual information (MI) of two random variables is a measure of the mutual dependence between the two variables.

![](./resources/images/venn_mutual_information.png)

![](./resources/images/tex_mutual_information.png)

