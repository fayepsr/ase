# Short PHP Documentation

## Table of Contents

| Method | Description |
|--------|-------------|
| [**Api**](#Api) |  |
| [Api::highlight](#Apihighlight) | This function returns the highlighted code. It returns either a full HTML document or a JSON |
| [Api::finetune](#Apifinetune) | It uses the finetune function of the model |
| [**ApiException**](#ApiException) |  |
| [ApiException::__construct](#ApiException__construct) |  |
| [**ApiExceptionHTML**](#ApiExceptionHTML) |  |
| [ApiExceptionHTML::__construct](#ApiExceptionHTML__construct) |  |
| [**Logger**](#Logger) |  |
| [Logger::log](#Loggerlog) |  |

## Api





* Full name: \Api


### Api::highlight

This function returns the highlighted code. It returns either a full HTML document or a JSON

```php
Api::highlight( string lang = '', string code = '', mixed secret = '', string mode = 'html' ): array
```



* This method is **static**.
**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `lang` | **string** |  |
| `code` | **string** |  |
| `secret` | **mixed** |  |
| `mode` | **string** | : Accepts html or JSON |






---
### Api::finetune

It uses the finetune function of the model

```php
Api::finetune( string lang = '', mixed secret = '' ): array
```



* This method is **static**.
**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `lang` | **string** |  |
| `secret` | **mixed** |  |






---
## ApiException





* Full name: \ApiException
* Parent class: 


### ApiException::__construct



```php
ApiException::__construct( mixed code, mixed message ): mixed
```




**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `code` | **mixed** |  |
| `message` | **mixed** |  |






---
## ApiExceptionHTML





* Full name: \ApiExceptionHTML
* Parent class: 


### ApiExceptionHTML::__construct



```php
ApiExceptionHTML::__construct( mixed code, mixed html ): mixed
```




**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `code` | **mixed** |  |
| `html` | **mixed** |  |





---
## Logger





* Full name: \Logger


### Logger::log



```php
Logger::log( mixed message, mixed level = Logger::INFO ): mixed
```



* This method is **static**.
**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `message` | **mixed** |  |
| `level` | **mixed** |  |






---
