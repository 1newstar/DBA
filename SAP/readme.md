#  SAP B1 ON Cloud架构搭建

> 2017-12-13 Booboo

[TOC]

## B1OD的搭建架构

`Windows + IIS + SAP + MSSQL`

额外的服务：

- 域控服务 
- https证书

## 服务器规格

| 服务                  | 数量   | 规格       |
| ------------------- | ---- | -------- |
| 域控服务                | 1    | 2核/4     |
| SLD服务               | 1    | 4核/8G    |
| MSSQL数据库服务          | 1    | 32核/128G |
| Presentation server | 1    | 32核/128G |
| B1其他组建使用新的机器        |      |          |

## SAP组成

### B1云控制中心 

>  web浏览器上的管理控制台 B/S 

* SLD service
* SLD agent

### 服务工具

* service manager
* DI server
* mailer
* Landscape Manager
  * Lense Manager

  * stem Landscape Directory

  * tension Manager

    等