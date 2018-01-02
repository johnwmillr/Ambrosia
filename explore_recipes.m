[NUM,TXT,RAW] = xlsread('allRecipes_v3.xlsx');
% ingredients = TXT(1,3:end)';
ingredients = TXT(1,8:end)';
amounts = NUM(:,6:end);
% amounts = NUM(:,3:end);
% amounts = NUM(:,2:end);
titles = TXT(2:end,1);
ratings = NUM(:,1);
recipeID = TXT(:,2);
counts = sum(amounts>0)';

flavor_labels = TXT(1,5:7);
flavors = NUM(:,3:5);

%% Exclude infrequently used ingredients
mask_high_counts = counts>5;
top_ingredients = ingredients(mask_high_counts)

recipes = amounts(:,mask_high_counts);
recipes = double(recipes>0);
[coeff,score,~,~,explained] = pca(recipes);

%%
n = 1;
n = n:n+1;
figure
H=biplot(coeff(:,n),'scores',score(: , n),'varlabels',ingredients(mask_high_counts),'obslabels',titles);
xlabel(sprintf('PC%d (%0.2f%% var. explained)',n(1),explained(n(1))),'fontsize',FS)
ylabel(sprintf('PC%d (%0.2f%% var. explained)',n(2),explained(n(2))),'fontsize',FS)

%% K-means
X = score(:,1:2);
[cidx,ctrs] = kmeans(X,2);
figure
plot(X(cidx==1,1),X(cidx==1,2),'r.', X(cidx==2,1),X(cidx==2,2),'b.')


%% Plot with ratings
n=4;
figure, hold on
mask = ratings==3;
axs(:,1) = plot(score(mask,n),score(mask,n+1),'ro','markerfacecolor','r');
mask = ratings==4;
axs(:,2) = plot(score(mask,n),score(mask,n+1),'go','markerfacecolor','g');
mask = ratings==5;
axs(:,3) = plot(score(mask,n),score(mask,n+1),'bo','markerfacecolor','b');

%% Try to condense ingredients
new_ingredients = ingredients;
for i = 1:length(ingredients)    
    for j = 1:sum(mask_high_counts)
        if contains(ingredients(i), top_ingredients(j))
            new_ingredients(i) = top_ingredients(j);
            disp([ingredients(i) ' --> ' new_ingredients(i)])
            break
        end
    end
end

%% Just the high counts again
mask_high_counts = counts>20;
top_ingredients = new_ingredients(mask_high_counts);



%%
name = 'mango-banana smoothie';
% name = 'blueberry oatmeal smoothie';
ingrds_in_smoothie = logical(amounts(strcmpi(titles,name),:));
top_ingrds_in_smoothie = logical(recipes(strcmpi(titles,name),:));
ingredients(ingrds_in_smoothie)
top_ingredients(top_ingrds_in_smoothie)













