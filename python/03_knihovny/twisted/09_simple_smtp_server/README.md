# Ukázka komunikace

## SMTP

```
Server: 220 smtp.example.com Simple Mail Transfer Service Ready
Client: HELO client.example.com
Server: 250 smtp.example.com

Client: MAIL FROM:<alice@example.com>
Server: 250 OK

Client: RCPT TO:<bob@example.com>
Server: 250 OK

Client: DATA
Server: 354 Start mail input; end with <CRLF>.<CRLF>

Client: Subject: Test Email
Client: From: alice@example.com
Client: To: bob@example.com
Client:
Client: Hello Bob,
Client: This is a test email sent using the base SMTP protocol.
Client:
Client: Regards,
Client: Alice
Client: .
Server: 250 OK: queued as 12345

Client: QUIT
Server: 221 smtp.example.com Service closing transmission channel
```

## ESMTP

```
Server: 220 smtp.example.com ESMTP Service Ready
Client: EHLO client.example.com
Server: 250-smtp.example.com greets client.example.com
Server: 250-AUTH LOGIN
Server: 250-PIPELINING
Server: 250 8BITMIME

Client: AUTH LOGIN
Server: 334 VXNlcm5hbWU6
Client: YWxpY2U=                (alice, base64-encoded)
Server: 334 UGFzc3dvcmQ6
Client: c2VjcmV0               (secret, base64-encoded)
Server: 235 Authentication successful

Client: MAIL FROM:<alice@example.com>
Server: 250 OK

Client: RCPT TO:<bob@example.com>
Server: 250 OK

Client: DATA
Server: 354 End data with <CRLF>.<CRLF>

Client: Subject: Test ESMTP Email
Client: From: alice@example.com
Client: To: bob@example.com
Client:
Client: Hello Bob,
Client: This is a test email sent using ESMTP with authentication.
Client:
Client: Regards,
Client: Alice
Client: .
Server: 250 OK: queued as 12345

Client: QUIT
Server: 221 smtp.example.com Service closing transmission channel
```

# Asynchronní kód

- prováděn pomocí třídy `Deferred`, reprezentuje úkol prováděný asynchronně

# Autentikace

```
user1     -> dXNlcjE=
password1 -> cGFzc3dvcmQx
```

## `Portal`

- vstupní brána pro přihlašování
- předává data mezi místy kontroly a zpracování

## `CredentialsChecker`

- kontroluje přihlašovací údaje ve vybraném formátu, těch může být i více
- `Portal` může mít více přidružených checkerů
  - správný se vybírá podle formátu přihlášení
  - formát je určený podle rozraní, které třída s údaji implementuje
- po úspěšném ověření údajů vrací tzv. `avatarId`
  - může to být cokoliv, co později `Realm` využije k identifikaci uživatele

## `Realm`

- z `avatarId` vrátí reprezentaci účtu
- účet je instance třídy implementující rozhraní, které daný protokol očekává

## `Challenger`

- implementuje rozhraní, se kterým počítá checker, nese přihlašovací údaje
