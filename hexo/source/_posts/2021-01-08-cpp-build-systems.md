---
title: C++构建工具比较
date: 2021-01-08 16:26:33
tags: cpp
---

近日，又对C++产生了兴趣。

C++可以说是我内心的阴影，之所以是内心的阴影，倒不是C++的语言本身使我无法理解，或不喜欢C++的某些特性。相反我一直对C++怀有很高的敬意。之所以说C++是我的阴影，主要是因为C++的工具链实在是太长太杂了。我不介意多花点时间来学习C++的语言特性，但是我实在不想浪费时间在工具的学习上面。我屡屡在尝试用C++做点东西的时候，都被环境的配置而感到厌烦而放弃。

最近，感觉 [Dear ImGui](https://github.com/ocornut/imgui) 这个项目有点意思，可以用来做点有趣的事情。于是我想再次挑战一下C++的项目，顺便看看社区是否有新的构建工具出来简化我的工作。

此前的工具 Make 缺点是项目越大越复杂，需要学习很多东西。还有 autotools , scons，也有一定学习成本。

最近出现的 google的Bazel、facebook的Buck 两个build system都可以用来构建C++。看了些对比主要缺点是对原有的生态兼容性比较差，往往需要源码导入。

可以选择的有CMake和Meson。目前看来是比较合适的选择，我决定有空尝试一下meson。

找到两个template项目 [meson-sample-project](https://github.com/tiernemi/meson-sample-project)  、 [cmake-project-template](https://github.com/kigster/cmake-project-template) 。拿这个模板直接改一改就可以创建一个c++项目了，这样我内心的恐惧感减少了很多。 

