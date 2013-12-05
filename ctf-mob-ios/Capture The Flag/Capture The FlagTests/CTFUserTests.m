//
//  CTFUserTests.m
//  Capture The Flag
//
//  Created by Tomasz Szulc on 03.12.2013.
//  Copyright (c) 2013 Tomasz Szulc. All rights reserved.
//

#import <XCTest/XCTest.h>
#import <OCMock/OCMock.h>
#import <RestKit/Testing.h>
#import "CTFUser.h"
#import "CoreDataService.h"
@interface CTFUserTests : XCTestCase

@end

@implementation CTFUserTests {
    CoreDataService *_service;
    RKObjectManager *_manager;
}

- (void)setUp {
    _service = [[CoreDataService alloc] initForUnitTesting];
    
    _manager = [[RKObjectManager alloc] init];
    RKManagedObjectStore *managedObjectStore = [[RKManagedObjectStore alloc] initWithManagedObjectModel:_service.managedObjectModel];
    _manager.managedObjectStore = managedObjectStore;
    
    NSBundle *bundle = [NSBundle bundleWithIdentifier:[[NSBundle mainBundle].bundleIdentifier stringByAppendingString:@"Tests"]];
    [RKTestFixture setFixtureBundle:bundle];
    
    [super setUp];
}

- (void)tearDown {
    _service = nil;
    _manager = nil;
    [super tearDown];
}


- (void)testUserResponseMApping {
    id parsedJSON = [RKTestFixture parsedObjectWithContentsOfFixture:@"user-response.json"];
    
    RKEntityMapping *mapping = [RKEntityMapping mappingForEntityForName:@"CTFUser" inManagedObjectStore:_manager.managedObjectStore];
    [mapping addAttributeMappingsFromDictionary:[CTFUser dictionaryForResponseMapping]];
    
    RKMappingTest *test = [RKMappingTest testForMapping:mapping sourceObject:parsedJSON destinationObject:nil];
    test.managedObjectContext = _service.managedObjectContext;
    
    RKPropertyMappingTestExpectation *usernameExpectation =
    [RKPropertyMappingTestExpectation expectationWithSourceKeyPath:@"username" destinationKeyPath:@"username"];
    [test addExpectation:usernameExpectation];

    RKPropertyMappingTestExpectation *emailExpectation =
    [RKPropertyMappingTestExpectation expectationWithSourceKeyPath:@"email" destinationKeyPath:@"email"];
    [test addExpectation:emailExpectation];

    RKPropertyMappingTestExpectation *passwordExpectation =
    [RKPropertyMappingTestExpectation expectationWithSourceKeyPath:@"password" destinationKeyPath:@"password"];
    [test addExpectation:passwordExpectation];
    
    RKPropertyMappingTestExpectation *nickExpectation =
    [RKPropertyMappingTestExpectation expectationWithSourceKeyPath:@"location" destinationKeyPath:@"location"];
    [test addExpectation:nickExpectation];
    
    [test verify];
}


@end
