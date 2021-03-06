# Entropy Wiki

| **TYPE**            | **EQUATION**                                                                                     | **VENN DIAGRAM**                                                                                  |
|---------------------|--------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------:|
| [Entropy](#entropy)             | ![](./resources/images/tex_entropy.png)             |                                               ![](./resources/images//venn_entropy_3.png)         |
| [Cross Entropy](#cross-entropy)       | ![](./resources/images/tex_cross_entropy.png)       | ![](./resources/images/venn_cross_entropy_2.png)       |
| [Relative Entropy](#relative-entropy)       | ![](./resources/images/tex_relative_entropy.png)       | ![](./resources/images/venn_relative_entropy_2.png)       |
| [Joint Entropy](#joint-entropy)       | ![](./resources/images/tex_joint_entropy.png)       | ![](./resources/images/venn_joint_entropy.png)       |
| [Conditional Entropy](#conditional-entropy) | ![](./resources/images/tex_conditional_entropy.png) | ![](./resources/images/venn_conditional_entropy.png) |
| [Mutual Information](#mutual-information)  | ![](./resources/images/tex_mutual_information.png)  | ![](./resources/images/venn_mutual_information.png)  |
| [Independent Entropy](#independent-entropy)  | ![](./resources/images/tex_independent_entropy.png)  | ![](./resources/images/venn_independent_entropy.png)  |


# Entropy

Information entropy is the average rate at which information is produced by a stochastic source of data. The measure of information entropy associated with each possible data value

![](./resources/images/tex_entropy.png)






![](./resources/images/entropy_intro/tree_basic.png)



<table width="100%">
  <tr>
    <th width="50%"><b>Example 1</b></th>
    <th width="50%"><b>Example 2</b></th>
  </tr>
  <tr>
    <td width="50%">In Example 1 Alice selects a random letter A, B, C, or D. Each with a 1/4 chance of being selected. If Bob had to guess which letter Alice chose with YES/NO questions, how many questions on average would you expect Bob to ask?</td>
    <td width="50%">In Example 2 Alice again selects a random letter, but this time the probabilities of each letter has changed to: A = 1/2, B = 1/4, C = 1/8 and D = 1/8. If Bob had to guess which letter Alice chose with YES/NO questions, how many questions on average would you expect Bob to ask?</td>
  </tr>
  <tr>
    <td width="50%" align="center"><img src="./resources/images/intro/symbol_a_alice_bob.png" /></td>
    <td width="50%" align="center"><img src="./resources/images/intro/symbol_b_alice_bob.png" /></td>
  </tr>
  <tr>
    <td width="100%" colspan="2">
      <p>Entropy is defined as the average number of yes/no question. To calculate the entropy we will figure out how many YES/NO each example requires. The most effcient way to guess the letter is to ask questions that split the remain choses in half.</p>
    </td>
    </tr>
    <tr> 
    <td width="100%" align="center" colspan="2">
      <img height="70%" widtch="70%" src="./resources/images/intro/entropy_explain_1.png" />
    </td>
  </tr>
  <tr>
    <td width="50%">In Example 1 The most efficient way for Bob to guess, with YES/NO question, which letter Alice chose is to make guesses that split the remaining choses in half. The following is an example for the give probabilities.</td>
    <td width="50%">In Example 2 Alice again selects a random letter, but this time the probabilities of each letter has changed to: A = 1/2, B = 1/4, C = 1/8 and D = 1/8. If Bob had to guess which letter Alice chose with YES/NO questions, how many questions on average would you expect Bob to ask?</td>
  </tr>
  <tr>
    <td width="50%" align="center"><img src="./resources/images/intro/symbol_a_questons.png" /></td>
    <td width="50%" align="center"><img src="./resources/images/intro/symbol_b_questons.png" /></td>
  </tr>
  <tr>
    <td width="100%" colspan="2" align="center">
      <img height="70%" widtch="70%" src="./resources/images/intro/entropy_explain_2.png" />
    </td>
  </tr>
  <tr>
    <td width="50%">In Example 1 Alice selects a random letter A, B, C, or D. Each with a 1/4 chance of being selected. If Bob had to guess which letter Alice chose with YES/NO questions, how many questions on average would you expect Bob to ask?</td>
    <td width="50%">In Example 2 Alice again selects a random letter, but this time the probabilities of each letter has changed to: A = 1/2, B = 1/4, C = 1/8 and D = 1/8. If Bob had to guess which letter Alice chose with YES/NO questions, how many questions on average would you expect Bob to ask?</td>
  </tr>
  <tr>
    <td width="50%" align="center"><img src="./resources/images/intro/symbol_a_num_questions_2.png" /></td>
    <td width="50%" align="center"><img src="./resources/images/intro/symbol_b_num_questions.png" /></td>
  </tr>
</table>



# Entropy Equation

![](./resources/images/intro/entropy_explain_1.png)

![](./resources/images/intro/entropy_explain_2.png)

![](./resources/images/intro/entropy_explain_3.png)



 
# Cross Entropy

In information theory, the cross entropy between two probability distributions *p* and *q* over the same underlying set of events measures the average number of bits needed to identify an event drawn from the set, if a coding scheme is used that is optimized for an "artificial" probability distribution *q*, rather than the "true" distribution *p*.

![](./resources/images/venn_cross_entropy_2.png)

![](./resources/images/tex_cross_entropy.png)

# Relative Entropy 
### ***(Kullback-Liebler Divergence)***


In mathematical statistics, the Kullback–Leibler divergence (also called relative entropy) is a measure of how one probability distribution is different from a second, reference probability distribution.

![](./resources/images/venn_relative_entropy_2.png)

![](./resources/images/tex_relative_entropy.png)

# Joint Entropy

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


# Independent Entropy

In probability theory and information theory, the mutual information (MI) of two random variables is a measure of the mutual dependence between the two variables.

![](./resources/images/venn_independent_entropy.png)

![](./resources/images/tex_independent_entropy.png)
