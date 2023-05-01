---------奇迹提问：在window下可以，在liunx上不可用-------------

element not interactable IN selenium?


iframe,switchToWindow报错--no such element: Unable to locate element
https://blog.csdn.net/wushuai150831/article/details/78648228
How to Find an Element by XPath in Selenium
What Is XPath?

https://blog.csdn.net/songlh1234/article/details/100983248
https://www.testim.io/blog/find-element-by-xpath-selenium/

https://blog.csdn.net/IT_LanTian/article/details/124352742

The "element not interactable" error in Selenium typically occurs when you try to interact with an element that is either not visible or not enabled on the web page.

To resolve this issue, you can try the following steps:

Wait for the element to become visible and enabled before interacting with it.
Ensure that the element is not within an iframe, as you may need to switch to the correct frame before interacting with it.
Check if the element is overlapped by another element or if there are any pop-ups that are blocking it.
Verify that the element locator is correct and matches the element you are trying to interact with.
If none of these solutions work, you may need to provide more information about the specific error message and your code so that we can further troubleshoot the issue.


-------------------
奇迹提问：在window下可以，在liunx上不可用

Selenium防踩坑 - Element is not clickable at point...

https://juejin.cn/post/7028451270029475847
https://blog.csdn.net/u012874140/article/details/108869803
--------------------------------------------

 奇迹提问：用div与button标签作为按钮的一些区别



单侧可以为什么一起执行结果不对呢？
 - 一个执行失败，剩余的不执行了。

selenium.common.exceptions.TimeoutException:
