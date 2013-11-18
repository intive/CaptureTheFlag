//
//  CTFCredentialValidatorTests.m
//  Capture The Flag
//
//  Created by Tomasz Szulc on 07.11.2013.
//  Copyright (c) 2013 Tomasz Szulc. All rights reserved.
//

#import <XCTest/XCTest.h>
#import "CTFCredentialsValidator.h"

@interface CTFCredentialValidatorTests : XCTestCase
@end

@implementation CTFCredentialValidatorTests

#pragma mark - CredentailTypeUsername
- (void)testUsernameLength
{
    XCTAssert([self validUsername:@"login"] == ValidationWrongCredentials, @"");
    XCTAssert([self validUsername:@"loginn"] == ValidationOK, @"");
    XCTAssert([self validUsername:@"thisisverylonglogin"] == ValidationWrongCredentials, @"");
}

- (void)testUsernameCharacters
{
    XCTAssert([self validUsername:@"login1"] == ValidationOK, @"");
    XCTAssert([self validUsername:@"123456"] == ValidationOK, @"");
    XCTAssert([self validUsername:@"_123456"] == ValidationWrongCredentials, @"");
    XCTAssert([self validUsername:@"_123d5_"] == ValidationWrongCredentials, @"");
    XCTAssert([self validUsername:@"valid!@__l"] == ValidationWrongCredentials, @"");
}

- (ValidationResult)validUsername:(NSString *)username
{
    return [CTFCredentialsValidator validCredential:username withType:CredentialTypeUsername];
}


#pragma mark - CredentialTypePassword
- (void)testPasswordLength
{
    XCTAssert([self validPassword:@"abc"] == ValidationWrongCredentials, @"");
    XCTAssert([self validPassword:@"ancdefgv"] == ValidationOK, @"");
    XCTAssert([self validPassword:@"123asd!@#%^|dggg66654"] == ValidationWrongCredentials, @"");
}

- (void)testPasswordCharacters
{
    XCTAssert([self validPassword:@"goodPass123!@#avc:)"] == ValidationOK, @"");
    XCTAssert([self validPassword:@"goodPassButWeak"] == ValidationOK, @"");
    XCTAssert([self validPassword:@"§1234567890-="] == ValidationOK, @"");
    XCTAssert([self validPassword:@"!@#$$%%^&*())"] == ValidationOK, @"");
    XCTAssert([self validPassword:@"this is not a password"] == ValidationWrongCredentials, @"");
}

- (ValidationResult)validPassword:(NSString *)password
{
    return [CTFCredentialsValidator validCredential:password withType:CredentialTypePassword];
}


#pragma mark - CredentialTypeEmail
- (void)testEmailCharacters
{
    XCTAssert([self validEmail:@"abc@abcd.pl"] == ValidationOK, @"");
    XCTAssert([self validEmail:@"abc.abcd@abc.abcd.pl"] == ValidationOK, @"");

    XCTAssert([self validEmail:@".%@.-.pl"] == ValidationWrongCredentials, @"");
    XCTAssert([self validEmail:@"@.pl"] == ValidationWrongCredentials, @"");
    XCTAssert([self validEmail:@".pl"] == ValidationWrongCredentials, @"");
    XCTAssert([self validEmail:@"a.pl"] == ValidationWrongCredentials, @"");
    XCTAssert([self validEmail:@"abc@abc"] == ValidationWrongCredentials, @"");
}

- (ValidationResult)validEmail:(NSString *)email
{
    return [CTFCredentialsValidator validCredential:email withType:CredentialTypeEmail];
}

@end