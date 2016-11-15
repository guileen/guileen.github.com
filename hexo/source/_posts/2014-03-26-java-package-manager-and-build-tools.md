---
title: Java包管理和構建工具
layout: post
published: true
categories: 
tags: [java, CI]
---

雖然不喜歡JAVA，但是想學Android，還是要重新撿起來它。但是已經習慣了npm如此方便的包管理工具的人已經無法適應沒有npm的生活了。

N年前，JAVA的構建都是用Ant進行的，但Ant只是專注於構建，並不做包管理。後來是Maven，maven既有構建工具，也有包管理（依賴管理）的功能。但是Maven的pom.xml寫起來實在冗長，不想寫。

於是重新去瞭解了一下，發現JAVA領域也已經產生了一些新的包管理和構建工具了。Gradle和Ivy。

Ivy 是Maven之後的又一個包管理工具。而Gradle則是基於groovy語言開發的一種java構建的DSL（領域專用語言 Domain-specific language）。

Ivy安裝前需要安裝Ant，Ivy本身是Ant的一個子項目。與Maven既做構建又做依賴的方法不同，Ivy只做依賴，而構建交給Ant來做。我比較喜歡Ant + Ivy這種模式，Maven過於耦合。
我們的Java項目下應該存在一個build.xml和一個ivy.xml，分別用於描述Ant構建過程和依賴。

### 使用Ant自动安装Ivy

[Ant自动安装Ivy](http://ant.apache.org/ivy/history/2.2.0/install.html)

```xml
<project name="demo" default="resolve" xmlns:ivy="antlib:org.apache.ivy.ant">
    <property name="ivy.install.version" value="2.2.0" />
    <condition property="ivy.home" value="${env.IVY_HOME}">
      <isset property="env.IVY_HOME" />
    </condition>
    <property name="ivy.home" value="${user.home}/.ant" />
    <property name="ivy.jar.dir" value="${ivy.home}/lib" />
    <property name="ivy.jar.file" value="${ivy.jar.dir}/ivy.jar" />

    <target name="download-ivy" unless="offline">
        <mkdir dir="${ivy.jar.dir}"/>
        <!-- download Ivy from web site so that it can be used even without any special installation -->
        <get src="http://repo2.maven.org/maven2/org/apache/ivy/ivy/${ivy.install.version}/ivy-${ivy.install.version}.jar" 
             dest="${ivy.jar.file}" usetimestamp="true"/>
    </target>

    <target name="init-ivy" depends="download-ivy">
      <!-- try to load ivy here from ivy home, in case the user has not already dropped
              it into ant's lib dir (note that the latter copy will always take precedence).
              We will not fail as long as local lib dir exists (it may be empty) and
              ivy is in at least one of ant's lib dir or the local lib dir. -->
        <path id="ivy.lib.path">
            <fileset dir="${ivy.jar.dir}" includes="*.jar"/>

        </path>
        <taskdef resource="org/apache/ivy/ant/antlib.xml"
                 uri="antlib:org.apache.ivy.ant" classpathref="ivy.lib.path"/>
    </target>
    
    <!-- ================================= 
      target: resolve              
     ================================= -->
    <target name="resolve" description="--> retrieve dependencies with ivy" depends="init-ivy">
        <ivy:retrieve />
    </target>
    
</project>
```

### ivy.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ivy-module version="2.0">
    <info organisation="org.apache" module="hello-ivy"/>
    <dependencies>
        <dependency org="commons-lang" name="commons-lang" rev="2.0"/>
        <dependency org="commons-cli" name="commons-cli" rev="1.0"/>
    </dependencies>
</ivy-module>
```

### ivysettings.xml



### Gradle

Gradle的職責是自動化構建，它同時支持Maven和Ivy包管理，甚至Ant的任務，比如這樣

build.gradle

```
task hello << {
    String greeting = 'hello from Ant'
    ant.echo(message: greeting)
}

task check << {
    ant.taskdef(resource: 'checkstyletask.properties') {
        classpath {
            fileset(dir: 'libs', includes: '*.jar')
        }
    }
    ant.checkstyle(config: 'checkstyle.xml') {
        fileset(dir: 'src')
    }
}
```

Java和XML是我最不喜歡的兩個東西，gradle可以讓構建不再是一堆雜亂冗長的XML了，而變成了一段優雅可讀的文字，很酷。但如果項目不是很大，構建不是很複雜，我覺得Ant+Ivy足夠了。
而維護一個複雜的構建過程時，Ant的build.xml一定會越來越亂，到那時，再切換至gradle不遲。
