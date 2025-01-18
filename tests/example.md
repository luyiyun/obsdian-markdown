===unordered_list_block_base===

- AAA
- BBB
- CCC

123455

===unordered_list_block_base===

===unordered_list_block_indented_content===

- aaa
  3456789
- bbb
  1234567
- cccc

123455
===unordered_list_block_indented_content===

===unordered_list_block_nest===

- aaa
  3456789
  - 123
  - 456
- bbb
  1234567
  - 789
  - 101
- cccc
  - 1
  - 2
  - 3

123455
===unordered_list_block_nest===

===unordered_list_block_with_code_block===

- aaa

  ```python
  print("Hello, world!")
  ```

- bbb
- cccc

  ```cpp
  #include <iostream>
  using namespace std;
  int main() {
    cout << "Hello, world!" << endl;
    return 0;
  }
  ```

123455
===unordered_list_block_with_code_block===

===ordered_list_block_base===

1. AAA
2. BBB
3. CCC

123455

===ordered_list_block_base===

===ordered_list_block_indented_content===

1. aaa
   3456789
2. bbb
   1234567
3. cccc

123455
===ordered_list_block_indented_content===

===ordered_list_block_with_code_block===

1. aaa

   ```python
   print("Hello, world!")
   ```

2. bbb
3. cccc

   ```cpp
   #include <iostream>
   using namespace std;
   int main() {
     cout << "Hello, world!" << endl;
     return 0;
   }
   ```

123455
===ordered_list_block_with_code_block===

===ordered_list_block_nest===

1. aaa
   3456789
   1. 123
   2. 456
2. bbb
   1234567
   1. 789
   2. 101
3. cccc
   1. 1
   2. 2
   3. 3

123455
===ordered_list_block_nest===

===task_list_base===

- [ ] aaa
- [ ] bbb
- [x] cccc

123455
===task_list_base===

===quote_base===

> This is a quote.

123455
===quote_base===

===quote_then_end===
> This is a quote.
===quote_then_end===

===quote_multi_lines===

> This is a quote.
> This is the second line of the quote.
> This is the third line of the quote.

===quote_multi_lines===

===paragraph_base===
AAAA
BBBB

CCCC

DDDD
===paragraph_base===

===front_matter_base===

---
title: Example
tags:

- tag1
- tag2
- tag3
author: admin
created: 2024-12-25 16:10
publish: true

---

1234

===front_matter_base===

===callout_base===

aaaaaa

## title

> [!warning]
> bbbbbb

cccccc
===callout_base===

===callout_wo_content===

> [!note]+ callout title

cccc

===callout_wo_content===

===callout_wo_succeed===

> [!note]+ callout title
===callout_wo_succeed===

===callout_title===

> [!note]+ callout title

cccc

===callout_title===

===callout_collapse===

> [!note]+ callout title

cccc

===callout_collapse===

===callout_nest===

aaaaaa

## title

> [!warning]
> bbbbbb
> > [!note]- nested
> > cccc

cccccc

===callout_nest===

===callout_code===

> [!note]
> bbbbbb
>
> ```python
> print("Hello, world!")
> ```

===callout_code===

===math_block_base===

aaaaaa

$$
a = b + 2
$$

cccccc

===math_block_base===

===horizontal_rule===

***
****
* * *
---
----
- - -
___
____
_ _ _

===horizontal_rule===

===code_block_base===
aaa

```python
print("Hello, world!")
```

bbb

===code_block_base===

===section_base===

# Section 1

12345

## Subsection 1.1

1234

# Section 2

456

===section_base===

===section_with_comment===

# Section 1

12345

## Subsection 1.1

1234

```python
# This is a comment
print(1234)
```

456

===section_with_comment===

===section_with_inline_code===

# Section 1

12345

## Subsection 1.1

1234 `print` function

456

===section_with_inline_code===

===footnote_base===

This is a simple footnote[^1].

[^1]: aaa
[^2]: bbb
  cccc
[^note]: dddd

xxxxxxxxxx

===footnote_base===

===footnote_end===

This is a simple footnote[^1].

[^1]: aaa
[^2]: bbb
  cccc
[^note]: dddd
===footnote_end===

===comment_block_base===
aaa
%%
This is a block comment.

Block comments can span multiple lines.
%%
bbb
===comment_block_base===

===table_base===
aaa

| First name | Last name |
| ---------- | --------- |
| Max        | Planck    |
| Marie      | Curie     |

bbb
===table_base===

===table_one_column===
| First name |
| ---------- |
| Max        |
| Marie      |
===table_one_column===

===table_simple===

First name | Last name
-- | --
Max | Planck
Marie | Curie

===table_simple===


===table_with_align===
Left-aligned text | Center-aligned text | Right-aligned text
:-- | :--: | --:
Content | Content | Content
===table_with_align===




