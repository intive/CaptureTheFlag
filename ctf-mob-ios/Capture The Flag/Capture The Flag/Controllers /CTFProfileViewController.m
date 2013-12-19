//
//  CTFProfileViewController.m
//  Capture The Flag
//
//  Created by Tomasz Szulc on 17.12.2013.
//  Copyright (c) 2013 Tomasz Szulc. All rights reserved.
//

#import "CTFProfileViewController.h"
#import "CTFAPIAccounts.h"
#import "CTFSession.h"
#import "CTFAPIConnection.h"

@interface CTFProfileViewController ()

@end

@implementation CTFProfileViewController {
    CTFAPIAccounts *_accounts;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    _accounts = [[CTFAPIAccounts alloc] initWithConnection:[CTFAPIConnection sharedConnection]];
    [_accounts accountInfoForToken:[CTFSession sharedInstance].token block:^(CTFUser *user) {
        NSLog(@"user = %@", user);
    }];
}

- (void)localizeUI {
    self.navigationItem.title = NSLocalizedString(@"view.profile.navigation.title", nil);
}

@end
