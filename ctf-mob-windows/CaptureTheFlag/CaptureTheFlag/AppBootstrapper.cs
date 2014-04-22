namespace CaptureTheFlag {
	using System;
	using System.Collections.Generic;
	using System.Windows.Controls;
	using Microsoft.Phone.Controls;
	using Caliburn.Micro;
    using CaptureTheFlag.ViewModels;
    using CaptureTheFlag.Services;

	public class AppBootstrapper : PhoneBootstrapperBase
	{
		PhoneContainer container;

		public AppBootstrapper()
		{
			Start();
		}

		protected override void Configure()
		{
			container = new PhoneContainer();
			if (!Execute.InDesignMode)
				container.RegisterPhoneServices(RootFrame);

            container.PerRequest<UserAccessPivotViewModel>();
            container.PerRequest<UserLoginViewModel>();
            container.PerRequest<UserRegistrationViewModel>();

            container.PerRequest<MainAppPivotViewModel>();
            container.PerRequest<GameViewModel>();
            container.PerRequest<GameMapViewModel>();
            container.PerRequest<ListGamesViewModel>();
            container.PerRequest<GameItemViewModel>();

            container.PerRequest<CharacterViewModel>();
            container.PerRequest<UserViewModel>();

            container.PerRequest<ICommunicationService, CommunicationService>();
            container.PerRequest<IGameModelService, GameModelService>();
            container.PerRequest<IUserModelService, UserModelService>();
            container.PerRequest<IMapModelService, MapModelService>();
            container.PerRequest<ILocationService, LocationService>();

            container.Singleton<GlobalStorageService>();

			AddCustomConventions();
		}

		protected override object GetInstance(Type service, string key)
		{
			var instance = container.GetInstance(service, key);
			if (instance != null)
				return instance;

			throw new InvalidOperationException("Could not locate any instances.");
		}

		protected override IEnumerable<object> GetAllInstances(Type service)
		{
			return container.GetAllInstances(service);
		}

		protected override void BuildUp(object instance)
		{
			container.BuildUp(instance);
		}

		static void AddCustomConventions()
		{
			ConventionManager.AddElementConvention<Pivot>(Pivot.ItemsSourceProperty, "SelectedItem", "SelectionChanged").ApplyBinding =
				(viewModelType, path, property, element, convention) => {
					if (ConventionManager
						.GetElementConvention(typeof(ItemsControl))
						.ApplyBinding(viewModelType, path, property, element, convention))
					{
						ConventionManager
							.ConfigureSelectedItem(element, Pivot.SelectedItemProperty, viewModelType, path);
						ConventionManager
							.ApplyHeaderTemplate(element, Pivot.HeaderTemplateProperty, null, viewModelType);
						return true;
					}

					return false;
				};

			ConventionManager.AddElementConvention<Panorama>(Panorama.ItemsSourceProperty, "SelectedItem", "SelectionChanged").ApplyBinding =
				(viewModelType, path, property, element, convention) => {
					if (ConventionManager
						.GetElementConvention(typeof(ItemsControl))
						.ApplyBinding(viewModelType, path, property, element, convention))
					{
						ConventionManager
							.ConfigureSelectedItem(element, Panorama.SelectedItemProperty, viewModelType, path);
						ConventionManager
							.ApplyHeaderTemplate(element, Panorama.HeaderTemplateProperty, null, viewModelType);
						return true;
					}

					return false;
				};
		}
	}
}