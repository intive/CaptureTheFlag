﻿using Caliburn.Micro;
using CaptureTheFlag.Messages;
using CaptureTheFlag.Models;
using CaptureTheFlag.Services;
using RestSharp;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;

namespace CaptureTheFlag.ViewModels.GameVVMs
{
    public class GameFieldsViewModel : Screen,  IHandle<PreGame>, IHandle<PublishModelRequest<PreGame>>
    {
        protected readonly INavigationService navigationService;
        protected readonly CommunicationService communicationService;
        protected readonly GlobalStorageService globalStorageService;
        private readonly IEventAggregator eventAggregator;
        protected RestRequestAsyncHandle requestHandle;// TODO: implement abort

        public GameFieldsViewModel(INavigationService navigationService, CommunicationService communicationService, GlobalStorageService globalStorageService, IEventAggregator eventAggregator)
        {
            DebugLogger.WriteLine(this.GetType(), MethodBase.GetCurrentMethod());
            this.navigationService = navigationService;
            this.communicationService = communicationService;
            this.globalStorageService = globalStorageService;
            this.eventAggregator = eventAggregator;

            IsFormAccessible = true;

            Game = new PreGame();

            NameTextBlock = "Name:";
            DescriptionTextBlock = "Description:";
            StartTimeTextBlock = "Start time:";
            MaxPlayersTextBlock = "Max players:";
            GameTypeTextBlock = "Game type:";
            VisibilityRangeTextBlock = "Visibility range:";
            ActionRangeTextBlock = "Action range:";
        }

        #region Message handling
        //public void Handle(GameModelMessage message)
        //{
        //    DebugLogger.WriteLine(this.GetType(), MethodBase.GetCurrentMethod(), "");
        //    switch(message.Status)
        //    {
        //        case GameModelMessage.STATUS.IN_STORAGE:
        //            Game = globalStorageService.Current.Games[message.GameModelKey];
        //            IsFormAccessible = true;
        //            break;
        //        case GameModelMessage.STATUS.UPDATE:
        //            globalStorageService.Current.Games[Game.Url] = Game;
        //            eventAggregator.Publish(new GameModelMessage() { GameModelKey = Game.Url, Status = ModelMessage.STATUS.UPDATED });
        //            break;
        //        case GameModelMessage.STATUS.SHOULD_GET:
        //            IsFormAccessible = false;
        //            break;
        //    }
        //}

        public void Handle(PreGame message)
        {
            DebugLogger.WriteLine(this.GetType(), MethodBase.GetCurrentMethod());
            Game = message;
        }

        public void Handle(PublishModelRequest<PreGame> message)
        {
            DebugLogger.WriteLine(this.GetType(), MethodBase.GetCurrentMethod());
            PublishModelResponse<PreGame> response = new PublishModelResponse<PreGame>(message, Game);
            eventAggregator.Publish(response);
        }
        #endregion

        #region ViewModel states
        protected override void OnActivate()
        {
            base.OnActivate();
            DebugLogger.WriteLine(this.GetType(), MethodBase.GetCurrentMethod(), "");
            eventAggregator.Subscribe(this);
        }

        protected override void OnDeactivate(bool close)
        {
            DebugLogger.WriteLine(this.GetType(), MethodBase.GetCurrentMethod(), "");
            globalStorageService.Current.Games[Game.Url] = Game;
            eventAggregator.Unsubscribe(this);
            base.OnDeactivate(close);
        }
        #endregion

        #region Model Properties
        private Authenticator authenticator;
        public Authenticator Authenticator
        {
            get { return authenticator; }
            set
            {
                if (authenticator != value)
                {
                    authenticator = value;
                    NotifyOfPropertyChange(() => Authenticator);
                }
            }
        }

        private PreGame game;
        public PreGame Game
        {
            get { return game; }
            set
            {
                if (game != value)
                {
                    game = value;
                    NotifyOfPropertyChange(() => Game);
                }
            }
        }

        private string gameModelKey;
        public string GameModelKey
        {
            get { return gameModelKey; }
            set
            {
                if (gameModelKey != value)
                {
                    gameModelKey = value;
                    NotifyOfPropertyChange(() => GameModelKey);
                }
            }
        }

        public string SelectedType
        {
            get
            {
                return Game.Types.FirstOrDefault(pair => pair.Value == Game.Type).Key;
            }
            set
            {
                Game.Type = Game.Types[value];
                NotifyOfPropertyChange(() => SelectedType);
            }
        }
        #endregion

        #region UI Properties
        private string nameTextBlock;
        public string NameTextBlock
        {
            get { return nameTextBlock; }
            set
            {
                if (nameTextBlock != value)
                {
                    nameTextBlock = value;
                    NotifyOfPropertyChange(() => NameTextBlock);
                }
            }
        }

        private string descriptionTextBlock;
        public string DescriptionTextBlock
        {
            get { return descriptionTextBlock; }
            set
            {
                if (descriptionTextBlock != value)
                {
                    descriptionTextBlock = value;
                    NotifyOfPropertyChange(() => DescriptionTextBlock);
                }
            }
        }

        private string startTimeTextBlock;
        public string StartTimeTextBlock
        {
            get { return startTimeTextBlock; }
            set
            {
                if (startTimeTextBlock != value)
                {
                    startTimeTextBlock = value;
                    NotifyOfPropertyChange(() => StartTimeTextBlock);
                }
            }
        }

        private string maxPlayersTextBlock;
        public string MaxPlayersTextBlock
        {
            get { return maxPlayersTextBlock; }
            set
            {
                if (maxPlayersTextBlock != value)
                {
                    maxPlayersTextBlock = value;
                    NotifyOfPropertyChange(() => MaxPlayersTextBlock);
                }
            }
        }

        private string gameTypeTextBlock;
        public string GameTypeTextBlock
        {
            get { return gameTypeTextBlock; }
            set
            {
                if (gameTypeTextBlock != value)
                {
                    gameTypeTextBlock = value;
                    NotifyOfPropertyChange(() => GameTypeTextBlock);
                }
            }
        }

        private string visibilityRangeTextBlock;
        public string VisibilityRangeTextBlock
        {
            get { return visibilityRangeTextBlock; }
            set
            {
                if (visibilityRangeTextBlock != value)
                {
                    visibilityRangeTextBlock = value;
                    NotifyOfPropertyChange(() => VisibilityRangeTextBlock);
                }
            }
        }

        private string actionRangeTextBlock;
        public string ActionRangeTextBlock
        {
            get { return actionRangeTextBlock; }
            set
            {
                if (actionRangeTextBlock != value)
                {
                    actionRangeTextBlock = value;
                    NotifyOfPropertyChange(() => ActionRangeTextBlock);
                }
            }
        }

        private bool isFormAccessible;
        public bool IsFormAccessible
        {
            get { return isFormAccessible; }
            set
            {
                if (isFormAccessible != value)
                {
                    isFormAccessible = value;
                    NotifyOfPropertyChange(() => IsFormAccessible);
                }
            }
        }
        #endregion


    }
}
