//
//  CTFLoginViewController.m
//  Capture The Flag
//
//  Created by Tomasz Szulc on 06.11.2013.
//  Copyright (c) 2013 Tomasz Szulc. All rights reserved.
//

#import "CTFLoginViewController.h"
#import "CTFUser.h"

#import "CTFAPICredentials.h"
#import "CTFAPIAccounts.h"
#import "CTFAPIConnection.h"

#import "CTFLocalCredentialsStore.h"
#import "CTFLocalCredentials.h"

@interface CTFLoginViewController ()

@end

@implementation CTFLoginViewController {
    CTFAPIAccounts *_accounts;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    [self localizeUI];

    [self configureTapBackground];
    [self configureTextFields];
}

- (void)localizeUI {
    self.navigationItem.title = NSLocalizedString(@"view.login.navigation.title", nil);
    _usernameTF.placeholder = NSLocalizedString(@"view.login.textField.username.placeholder", nil);
    _passwordTF.placeholder = NSLocalizedString(@"view.login.textField.password.placeholder", nil);
    [_loginBtn setTitle:NSLocalizedString(@"view.login.button.login.title", nil) forState:UIControlStateNormal];
    [_registerBtn setTitle:NSLocalizedString(@"view.login.button.register.title", nil) forState:UIControlStateNormal];
}

- (void)configureTapBackground {
    UITapGestureRecognizer *gesture = [[UITapGestureRecognizer alloc] initWithTarget:self action:@selector(backgroundTapped)];
    [self.view addGestureRecognizer:gesture];
}

- (void)backgroundTapped {
    [self.view endEditing:YES];
}

- (IBAction)loginPressed
{
    NSString *username = _usernameTF.text;
    NSString *password = _passwordTF.text;
    
    CredentialsValidationResult result =
    [CTFAPICredentials validateSignInCredentialsWithUsername:username password:password];
    
    if (result == CredentialsValidationResultOK) {
        _statusLabel.text = NSLocalizedString(@"view.login.label.status.logged", nil);
        [self.view endEditing:YES];
        
        /// If successfuly logged to the server token will be provide in response
        _accounts = [[CTFAPIAccounts alloc] initWithConnection:[CTFAPIConnection sharedConnection]];
        [_accounts signInWithUsername:username andPassword:password withBlock:^(NSString *token) {
            
            if (token) {
                CTFUser *user = [CTFUser createObject];
                user.username = username;
                
                /// Store login and password in the Keychain
                CTFLocalCredentials *credentials = [[CTFLocalCredentials alloc] initWithUsername:username password:password];
                BOOL stored = [[CTFLocalCredentialsStore sharedInstance] storeCredentials:credentials];
                
                if (stored) {
                    /// Create new view and show
                    UIStoryboard *storyboard = [UIStoryboard storyboardWithName:@"Main" bundle:nil];
                    UINavigationController *mainNavigationController = [storyboard instantiateViewControllerWithIdentifier:NSStringFromClass([UINavigationController class])];
                    [self presentViewController:mainNavigationController animated:YES completion:^{
                        _usernameTF.text = @"";
                        _passwordTF.text = @"";
                        _statusLabel.text = @"";
                    }];
                } else {
#warning - [tsu] something goes wrong. Check what may goes wrong and improve this case
                }
            } else {
#warning - [tsu] need implementation of UIAlertView which shows appropriate alert that user can't login... Need some error handling
            }
        }];
    } else
    {
        _statusLabel.text = NSLocalizedString(@"view.login.label.status.wrong_credentials", nil);
    }
}

- (void)configureTextFields {
    [_usernameTF addTarget:self action:@selector(textFieldDidChange) forControlEvents:UIControlEventEditingChanged];
    [_passwordTF addTarget:self action:@selector(textFieldDidChange) forControlEvents:UIControlEventEditingChanged];
}

- (void)textFieldDidChange {
    CredentialsValidationResult result =
    [CTFAPICredentials validateSignInCredentialsWithUsername:_usernameTF.text password:_passwordTF.text];
    
    [_loginBtn setEnabled:(result == CredentialsValidationResultOK)];
}


#pragma mark - UITextFieldDelegate
- (BOOL)textFieldShouldReturn:(UITextField *)textField {
    [textField resignFirstResponder];
    return YES;
}


#pragma mark - Segues
- (BOOL)shouldPerformSegueWithIdentifier:(NSString *)identifier sender:(id)sender {
    if ([identifier isEqualToString:@"ToRegisterSegue"])
        return YES;
    return NO;
}

@end
